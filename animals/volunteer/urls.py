from django.urls import path
from .views import VolunteerApplicationView

urlpatterns = [
    path('volunteer/applications/', VolunteerApplicationView.as_view(), name='volunteer-applications'),
    path('volunteer/applications/<int:pk>/', VolunteerApplicationView.as_view(), name='volunteer-applications-detail'),
]