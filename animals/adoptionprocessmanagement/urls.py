from django.urls import path
from .views import AdoptionApplicationCreateView

urlpatterns = [
    path("adoption-applications/create/", AdoptionApplicationCreateView.as_view(), name="create-adoption-application"),
]