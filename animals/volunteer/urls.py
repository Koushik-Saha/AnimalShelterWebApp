from django.urls import path
from .views import VolunteerApplicationView, VolunteerProfileView

urlpatterns = [
    path('applications/', VolunteerApplicationView.as_view(), name='volunteer-applications'),
    path('applications/<int:pk>/', VolunteerApplicationView.as_view(), name='volunteer-applications-detail'),

    path('volunteers/profiles/', VolunteerProfileView.as_view(), name='volunteer-profiles'),
]