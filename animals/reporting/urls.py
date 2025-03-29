from django.urls import path
from .views import ReportView, DashboardKPIView

urlpatterns = [
    path('reports/', ReportView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/', ReportView.as_view(), name='report-detail'),

    path("dashboard/kpis/", DashboardKPIView.as_view(), name="dashboard-kpis"),
]
