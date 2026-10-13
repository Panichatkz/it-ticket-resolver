markdown# 🏢 AI-Powered Internal IT Service Desk Platform
### End-to-End Documentation Manual for Non-Technical Users & System Administrators

Welcome to the documentation handbook for the **Internal IT Service Desk Platform**. This platform is a completely localized, offline software application designed to automate how internal technical issues are prioritized, routed, and managed across the company. 

Unlike traditional ticketing systems that rely on humans to read, evaluate, and assign tickets manually, this platform utilizes a custom **Multi-Input Multiple-Output (MIMO) Deep Learning Engine**. By learning from historical company patterns, the system automatically evaluates an incoming problem description alongside employee metadata, makes three independent operational decisions simultaneously, and audits the transaction instantly to a secure local database.

---

## 📑 Table of Contents
1. [Core Platform Goals: What and Why](#1-core-platform-goals-what-and-why)
2. [How the AI Model Works (In Plain English)](#2-how-the-ai-model-works-in-plain-english)
3. [The MVT Software Architecture Blueprint](#3-the-mvt-software-architecture-blueprint)
4. [Step-by-Step Offline Installation Guide](#4-step-by-step-offline-installation-guide)
5. [The Step-by-Step Data Flow: What Happens Where](#5-the-step-by-step-data-flow-what-happens-where)
6. [Advanced Features: Automated Safeguards & Reporting](#6-advanced-features-automated-safeguards--reporting)
7. [Operational Troubleshooting Handbook](#7-operational-troubleshooting-handbook)

---

## 1. Core Platform Goals: What and Why

In traditional corporate environments, a standard IT Service Desk suffers from three primary operational bottlenecks:
*   **Manual Triaging Delays:** A human dispatcher must manually open every incoming email or form submission, evaluate the emergency level, and forward it to a specific engineering queue. This creates human bottlenecks.
*   **Inaccurate Priority Assignment:** End-users often classify every ticket as "Urgent" or "Critical" regardless of actual severity, causing Level 2 and Level 3 engineering squads to become overwhelmed by minor desktop issues.
*   **Unpredicted SLA Violations:** Service Level Agreements (SLAs) dictating resolution deadlines are typically fixed values based solely on categories, failing to account for user or software variations.

### The Automated Solution
This platform addresses those challenges by combining deep-learning automation with traditional deterministic business logic. It takes three distinct input streams—**Text**, **Categories**, and **Continuous Numbers**—and simultaneously resolves three critical operational targets:
1.  **Urgency Classification:** Determining if an incident is a P1 (Critical), P2 (High), P3 (Medium), or P4 (Low) event.
2.  **Queue Target Routing:** Forwarding the ticket instantly to the Level 1 Helpdesk, Level 2 Network Operations, or Level 3 Systems Administration squad.
3.  **SLA Time Regression:** Dynamically predicting a continuous continuous value (the exact number of hours required to clear the issue) tailored to the historical complexity of the specific system component.

---

## 2. How the AI Model Works (In Plain English)

The machine learning core of this application is built using a **Multiple-Input Multiple-Output (MIMO)** neural network framework. To non-technical users, think of a traditional AI model as a single assembly line: it takes one input (e.g., text) and makes one single decision (e.g., sentiment analysis). 

Our MIMO framework acts like a **central dispatch brain** that receives several data modalities simultaneously and splits its conclusions into independent, parallel task managers.

Use code with caution.[ INPUT STREAMS ]                   [ CENTRAL FUSION ENGINE ]              [ SIMULTANEOUS INFERENCES ]┌───────────────────────────┐│ 1. TEXT DESCRIPTION       │ ───► Word Indexing & Embedding├───────────────────────────┤                                               ┌───► 🔴 Impact Urgency (P1 - P4)│ 2. CATEGORICAL CODES      │ ───► Structural Feature Concat Matrix ───────┼───► ⚙️ Engineering Queue Assignment├───────────────────────────┤                                               └───► ⏱️ Estimated SLA Hours Window│ 3. METRIC INDICATORS      │ ───► Numeric Normalization Layers└───────────────────────────┘
### The Three Independent Data Input Channels:
*   **Text Processing Branch:** The model takes raw human language (Subject Lines and Error Logs) and parses it using a **Text Vectorization** layer. It strips out punctuation, converts strings into numbers based on a corporate dictionary vocabulary index, and maps them to dense arrays. This allows the network to learn that phrases like *"Switch Blown"* or *"403 Forbidden"* indicate a highly technical network issue.
*   **Categorical Context Branch:** The model ingests structural category indicators—the specific **Asset Category Type** (e.g., Laptop, Switch, Core Server) and the **Department** submitting the issue. The model uses an embedding layer to learn the relationships between these groups (e.g., a ticket from the *Finance Unit* regarding *Payroll Software* is traditionally a high-impact combination).
*   **Numerical Metrices Branch:** The system accepts continuous floating-point variables representing business conditions: **Employee Tenure (Years)** and the **Software/OS Patch Version**. This ensures that issues affecting complex legacy software versions or submitted by senior leaders can be dynamically adjusted.

---

## 3. The MVT Software Architecture Blueprint

The web application is structured using Python's highly robust **MVT (Model-View-Template)** architecture. This structure completely decouples the user interface from the database layer and the deep learning runtime.

┌──────────────────────────────────────────────┐│         PRESENTATION TEMPLATE LAYER          ││             (ticket_form.html)               │└──────────────────────────────────────────────┘│▼ Async AJAX Fetch Request (JSON Data Payload)┌──────────────────────────────────────────────┐│            LOGIC CONTROLLER VIEW             ││                 (views.py)                   │ <─── [ Keras RAM Cache Cache ]└──────────────────────────────────────────────┘│▼ Validated Native BSON Document Object┌──────────────────────────────────────────────┐│           PERSISTENT DATABASE STORE          ││             (MongoDB Data Ledger)            │└──────────────────────────────────────────────┘
The system is organized into a clean folder structure designed for easy maintenance and zero network cross-talk:
*   **`training_pipeline.ipynb` (The AI Sandbox):** A standalone Jupyter Notebook workspace used by data analysts to load data from an offline CSV spreadsheet file, configure the neural network layout, run training iterations, and export the final optimized configurations to a single binary weight file (`it_mimo_model.keras`).
*   **`ticketing_app/apps.py` (The Memory Cache Manager):** An internal initialization layer that loads the multi-megabyte Keras `.keras` binary file into your laptop's RAM memory exactly once when the server boots. This prevents file-loading bottlenecks and keeps response times fast when multiple users submit tickets.
*   **`ticketing_app/views.py` (The Controller view):** The operational core that receives front-end form data, converts incoming text sentences into numeric index codes via the cached vectorizer, runs the model, applies business safeguard rules, and writes data documents straight to MongoDB.
*   **`ticketing_app/templates/` (The Presentation Layer):** Standalone HTML text files containing user forms and dynamic historical logging tables rendered directly from database queries.

---

## 4. Step-by-Step Offline Installation Guide

This entire application operates **100% locally and offline**. It requires no external cloud connections, API subscriptions, or external network data consumption.

### Prerequisites Verification:
Ensure you have the following software installed natively on your local Windows laptop:
1.  **Anaconda / Miniconda Distribution Engine**
2.  **MongoDB Community Server Edition** (Ensure the MongoDB Windows background service is active and listening on standard port `27017`).

### 1. Open Anaconda Prompt & Target Directory
Press your Windows key, type **Anaconda Prompt**, open the console window, and navigate directly into your project root folder:
```cmd
cd C:\Users\ST\it_mimo_django
```

### 2. Verify Offline Core Libraries Installation
Execute the package installer command to configure all required background libraries inside your active environment:
```cmd
pip install django numpy keras tensorflow pymongo requests pandas openpyxl notebook
```

---

## 5. The Step-by-Step Data Flow: What Happens Where

To understand how data flows through the application end-to-end, follow this execution trace from the moment an employee hits submit:

### Step A: Data Entry & Presentation Capture
*   **Location:** The web browser (`http://127.0.0` rendering layout `ticket_form.html`).
*   **What happens:** The user types a description (e.g., *"Database corruption error"*), picks their device asset from a dropdown, and clicks the submission button. 
*   **The technology:** An asynchronous JavaScript `fetch()` block captures the input fields, attaches Django's cross-site request protection token (`X-CSRFToken`) for data security, packages everything into a compact JSON data payload, and sends it to the server without reloading the browser tab.

### Step B: The Central Processing view Controller
*   **Location:** The backend web controller (`ticketing_app/views.py` via view routing endpoint function `ticket_form_view`).
*   **What happens:** The server interceptor accepts the JSON string payload and extracts the individual variables. 
*   **Pre-Vectorization Check:** The raw string input sentence is piped through the pre-loaded `vectorizer_layer` cache. The text is instantly mapped to a static array structure of 40 integers.

### Step C: Keras Parallel Inference Computations
*   **Location:** The system RAM cache engine.
*   **What happens:** The server passes the numeric text vectors, categorical options matrix, and numerical indicators variables down to the pre-loaded `it_mimo_model` object.
*   **The math:** The model evaluates layer interactions across its trained weights and returns an array of floating-point probabilities matching each target configuration layer. The Python controller uses `np.argmax()` to select the highest-probability outcome index for each task.

### Step D: Database Persistence
*   **Location:** Local MongoDB Database Storage System.
*   **What happens:** The view structures a BSON document mapping your text input fields, descriptive text labels, and the AI's predictions along with an automated UTC timestamp.
*   **The technology:** The system uses the native `pymongo` driver to inject the record directly into your local storage collection (`ml_routed_tickets`), instantly generating a unique 24-character hexadecimal tracking trace ID.

---

## 6. Advanced Features: Automated Safeguards & Reporting

This platform includes several enterprise-grade operational safety features built on top of the raw machine learning logic:

### A. The Deterministic Business Rule Override Engine
Deep learning models can occasionally produce unpredictable classifications if an input sentence contains unusual slang or text variations. To protect critical company infrastructure, we implemented a **Deterministic Keyword Override Engine** directly inside the controller path.
*   **How it works:** The views layer maintains a protected list of core infrastructure terms (e.g., *"Server Down"*, *"Data Breach"*, *"Ransomware"*, *"Database Corrupt"*). 
*   **The safeguard:** If any of these exact keyword combinations hit an incoming issue text description string, the application automatically bypasses the AI's prediction. It forces the ticket priority straight to `P1 - Critical`, routes it immediately to the specialized engineering team, and locks down the predicted SLA resolution target window to a strict timeline of `1.0 Hours`—guaranteeing operational safety regardless of model training fluctuations.

### B. High-Fidelity Offline Excel Analytics Reporting Engine
For corporate stakeholders and service managers who want to audit IT desk performance without accessing code terminals, the platform features a complete data export ecosystem.
*   **How it works:** When a user navigates to the **Historical Audit Ledger** view page and clicks the green download button, an automated script executes a full search query against your local MongoDB data cluster.
*   **The technology:** The script converts the raw document structures into a structured `pandas` DataFrame matrix, streams the binary data layout onto your storage cells using the `openpyxl` writing tool, and pushes a standard Excel spreadsheet report directly to your desktop downloads folder completely offline.

---

## 7. Operational Troubleshooting Handbook

If you experience unexpected behavior or errors while managing the local application platform, check this quick reference guide:

### Symptom: `Bad Request 400` or `Server Error Msg` displayed on form submission
*   **The cause:** The numeric conversion layers failed to parse an input field. If an empty value string or an alpha character text block is passed inside the numerical indicator input boxes (Tenure or Version), the casting utility fails inside your view logic.
*   **The fix:** Always make sure the number text inputs on your form layout contain valid decimals or standard integers before clicking the submit button. Ensure your JavaScript contains the default `|| 0` parameter protections.

### Symptom: Connection error: `Unexpected token '<'`
*   **The cause:** The backend Python script threw a hidden runtime error, causing Django to return a standard HTML error webpage structure rather than data values.
*   **The fix:** Open your active **Windows Anaconda Prompt** window running the server script. Scroll to the bottom lines of the console logs stack trace to view the exact line and property name triggering the python crash.

### Symptom: Application stalls indefinitely on "Processing model evaluations..."
*   **The cause:** Your local MongoDB background service daemon has gone dormant or turned off.
*   **The fix:** Open your Windows Service Manager (search for `services.msc` from your desktop search bar), locate the service named **MongoDB Server**, right-click it, and select **Start / Restart** to clear port `27017` instantly.
