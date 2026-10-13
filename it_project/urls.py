from django.urls import path
from ticketing_app import views

urlpatterns = [
    path('', views.ticket_form_view, name='ticket_form'),
    path('logs/', views.data_logs_view, name='data_logs'),
    path('logs/export/', views.export_excel_view, name='export_excel'), # <── ADD THIS ENDPOINT ROUTE
]
