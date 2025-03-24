from django.urls import path
from .views import (
    AnimalIntakeListCreateView,
    AnimalIntakeDetailView,
    AnimalIntakeUpdateView,
    AnimalIntakeDeleteView, AnimalIntakeListView
)

urlpatterns = [
    path('', AnimalIntakeListCreateView.as_view(), name="animal-intake-list-create"),
    path("list/", AnimalIntakeListView.as_view(), name="animal-intake-list"),
    path('<int:pk>/', AnimalIntakeDetailView.as_view(), name="animal-intake-detail"),
    path('<int:pk>/update/', AnimalIntakeUpdateView.as_view(), name="animal-intake-update"),
    path('<int:pk>/delete/', AnimalIntakeDeleteView.as_view(), name="animal-intake-delete"),

]