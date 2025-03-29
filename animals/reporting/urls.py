from django.urls import path
from .views import ReportView, DashboardKPIView, ReportCSVExportView

urlpatterns = [
    path('reports/', ReportView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/', ReportView.as_view(), name='report-detail'),

    path("dashboard/kpis/", DashboardKPIView.as_view(), name="dashboard-kpis"),

    path('reports/export/csv/', ReportCSVExportView.as_view(), name='report-export-csv'),

]
