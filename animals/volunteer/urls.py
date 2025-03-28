from django.urls import path
from .views import VolunteerApplicationView

urlpatterns = [
    path('applications/', VolunteerApplicationView.as_view(), name='volunteer-applications'),
    path('applications/<int:pk>/', VolunteerApplicationView.as_view(), name='volunteer-applications-detail'),
]