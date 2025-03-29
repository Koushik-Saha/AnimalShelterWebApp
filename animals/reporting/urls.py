from django.urls import path
from .views import ReportView

urlpatterns = [
    path('reports/', ReportView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/', ReportView.as_view(), name='report-detail'),
]
