from django.urls import path
from .views import AnimalIntakeCreateView

urlpatterns = [
    path("create/", AnimalIntakeCreateView.as_view(), name="animal-intake-create"),
]