from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('warehouse/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('pickup/', views.pickup_dashboard, name='pickup_dashboard'),
    path('products/', views.products_list, name='products_list'),
    path('sectors/', views.sectors_list, name='sectors_list'),
    path('requests/', views.requests_list, name='requests_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    
    # Отчеты
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/list/', views.reports_list, name='reports_list'),
    path('reports/<int:report_id>/', views.view_report, name='view_report'),
    path('reports/<int:report_id>/download/<str:file_type>/', views.download_report, name='download_report'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('api/chart-data/<str:chart_type>/', views.chart_data_api, name='chart_data_api'),
]