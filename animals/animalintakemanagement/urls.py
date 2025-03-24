from django.urls import path
from .views import (
    AnimalIntakeListCreateView,
    AnimalIntakeDetailView,
    AnimalIntakeUpdateView,
    AnimalIntakeDeleteView
)

urlpatterns = [
    path('', AnimalIntakeListCreateView.as_view(), name="animal-intake-list-create"),
    path('<int:pk>/', AnimalIntakeDetailView.as_view(), name="animal-intake-detail"),
    path('<int:pk>/update/', AnimalIntakeUpdateView.as_view(), name="animal-intake-update"),
    path('<int:pk>/delete/', AnimalIntakeDeleteView.as_view(), name="animal-intake-delete"),
]