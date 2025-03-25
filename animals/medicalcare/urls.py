from django.urls import path
from .views import MedicalRecordCreateView, MedicalRecordListView, MedicalRecordDetailView, MedicalRecordUpdateView, \
    MedicalRecordDeleteView

urlpatterns = [
    path('create/', MedicalRecordCreateView.as_view(), name='medical-create'),
    path('list/', MedicalRecordListView.as_view(), name='medical-list'),
    path('<int:pk>/', MedicalRecordDetailView.as_view(), name='medical-detail'),
    path('<int:pk>/update/', MedicalRecordUpdateView.as_view(), name='medical-update'),
    path('<int:pk>/delete/', MedicalRecordDeleteView.as_view(), name='medical-delete'),
]