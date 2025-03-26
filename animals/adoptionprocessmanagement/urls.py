from django.urls import path
from .views import AdoptionApplicationCreateView, AdoptionApplicationListView, AdoptionApplicationDetailView

urlpatterns = [
    path("adoption-applications/create/", AdoptionApplicationCreateView.as_view(), name="create-adoption-application"),

    path("adoption-applications/", AdoptionApplicationListView.as_view(), name="list-adoption-applications"),
    path("adoption-applications/<int:pk>/", AdoptionApplicationDetailView.as_view(), name="detail-adoption-application"),
]