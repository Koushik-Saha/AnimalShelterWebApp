from django.urls import path
from .views import MedicationCreateView, MedicationListView, MedicationDetailView

urlpatterns = [
    path('create/', MedicationCreateView.as_view(), name="create-medication"),
    path('<int:pk>/', MedicationDetailView.as_view(), name="medication-detail"),
    path('animal/<int:animal_id>/', MedicationListView.as_view(), name="animal-medication-list"),
]