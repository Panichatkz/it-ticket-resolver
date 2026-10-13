import json
import datetime
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from ticketing_app.apps import TicketingAppConfig

# Direct connection variables to local MongoDB background instance
db_client = MongoClient(settings.MONGODB_URI)
db = db_client[settings.MONGODB_NAME]
tickets_collection = db["ml_routed_tickets"]

# MVT Conversions labels map
URGENCY_LABELS = {0: "P1 - Critical", 1: "P2 - High", 2: "P3 - Medium", 3: "P4 - Low"}
ROUTING_LABELS = {0: "Service Desk (L1)", 1: "Network Ops (L2)", 2: "SysAdmin (L3)"}
ASSET_LABELS = {0: "Workstation / Laptop", 1: "Network Switch / Router", 2: "Corporate Server", 3: "Payroll Cloud Software"}
DEPT_LABELS = {0: "Finance Operations", 1: "Human Resources", 2: "Core Engineering", 3: "Logistics Fleet"}

CRITICAL_OVERRIDE_KEYWORDS = ["server down", "database corrupt", "data breach", "ransomware", "switch blown"]

def ticket_form_view(request):
    if request.method == "GET":
        return render(request, "ticket_form.html")
        
    elif request.method == "POST":
        try:
            payload = json.loads(request.body)
            txt = str(payload.get("subject_text", ""))
            dev = int(payload.get("asset_category", 0))
            dept_code = int(payload.get("department_org", 0))
            employee_tenure = float(payload.get("employee_tenure", 1.0))
            software_version = float(payload.get("software_version", 1.0))
            
            model = TicketingAppConfig.cached_mimo_model
            vectorizer = TicketingAppConfig.cached_vectorizer
            
            if model is None:
                p_urgency, p_route, p_sla = "P2 - High", "Service Desk (L1)", 4.5
            else:
                # 1. Processing Text inputs array vector
                vectorized_text = vectorizer(list([txt])).numpy()
                
                # 2. Processing Categorical matrix indicators
                vectorized_categories = np.array([[dev, dept_code]], dtype=np.int32)
                
                # 3. Processing Numerical indicator streams
                vectorized_numbers = np.array([[employee_tenure, software_version]], dtype=np.float32)
                
                # Execute simultaneous multi-output predictions pass
                preds = model.predict([vectorized_text, vectorized_categories, vectorized_numbers], verbose=0)
                
                # FIXED: Separate the multi-output list indices into distinct array targets 
                # before running argmax, resolving the inhomogeneous shape crash!
                urgency_preds_array = preds[0]
                routing_preds_array = preds[1]
                sla_preds_array = preds[2]
                
                p_urgency = URGENCY_LABELS.get(int(np.argmax(urgency_preds_array)), "Unknown Urgency")
                p_route = ROUTING_LABELS.get(int(np.argmax(routing_preds_array)), "Unknown Queue")
                p_sla = float(sla_preds_array[0][0]) if hasattr(sla_preds_array, "shape") else float(sla_preds_array)

            # Business Safeguards Rule Engine Override Checks
            is_overridden = False
            lower_text = txt.lower()
            if any(keyword in lower_text for keyword in CRITICAL_OVERRIDE_KEYWORDS):
                p_urgency = "P1 - Critical"
                p_route = "Network Ops (L2)" if dev == 1 else "SysAdmin (L3)"
                p_sla = 1.0
                is_overridden = True

            doc = {
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_text": txt,
                "device_category_label": ASSET_LABELS.get(dev, "Other Asset"),
                "department_label": DEPT_LABELS.get(dept_code, "Other Dept"),
                "employee_tenure_years": employee_tenure,
                "software_patch_version": software_version,
                "ai_mimo_inferences": {
                    "urgency_classification": p_urgency,
                    "routing_target_queue": p_route,
                    "sla_resolution_hours": round(max(0.5, p_sla), 2),
                    "rule_engine_override": is_overridden
                }
            }
            inserted_id = tickets_collection.insert_one(doc).inserted_id
            
            return JsonResponse({
                "status": "success",
                "predictions": {
                    "urgency": p_urgency,
                    "assigned_team": p_route,
                    "sla_time": f"{round(max(0.5, p_sla), 1)} Hours",
                    "override_active": is_overridden
                },
                "database_log": f"Logged with ID Trace Reference: {inserted_id}"
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

def data_logs_view(request):
    historical_tickets = list(tickets_collection.find().sort("_id", -1).limit(100))
    return render(request, "data_logs.html", {"tickets": historical_tickets})

def export_excel_view(request):
    try:
        raw_data = list(tickets_collection.find())
        if not raw_data:
            return HttpResponse("No records located to generate report.", status=400)
            
        flat_records = []
        for entry in raw_data:
            flat_records.append({
                "Incident ID": str(entry["_id"]),
                "Timestamp UTC": entry.get("timestamp"),
                "Problem Statement Description": entry.get("ticket_text"),
                "Asset Category": entry.get("device_category_label"),
                "Department Unit": entry.get("department_label"),
                "User Tenure (Years)": entry.get("employee_tenure_years"),
                "Patch Version": entry.get("software_patch_version"),
                "Urgency Outcome": entry.get("ai_mimo_inferences", {}).get("urgency_classification"),
                "Assigned Engineering Queue": entry.get("ai_mimo_inferences", {}).get("routing_target_queue"),
                "SLA Resolution Target (Hours)": entry.get("ai_mimo_inferences", {}).get("sla_resolution_hours"),
                "Bypass Rule Override Active": entry.get("ai_mimo_inferences", {}).get("rule_engine_override")
            })
            
        df = pd.DataFrame(flat_records)
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="IT_MIMO_Incident_Audit_Report.xlsx"'
        
        with pd.ExcelWriter(response, engine="openpyxl") as excel_writer:
            df.to_excel(excel_writer, index=False, sheet_name="MIMO Audit Records Ledger")
            
        return response
    except Exception as e:
        return HttpResponse(f"Reporting compilation fault: {e}", status=500)
