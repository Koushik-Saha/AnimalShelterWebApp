from django.urls import path
from .views import VolunteerApplicationView, VolunteerProfileView, VolunteerScheduleView, VolunteerActivityView

urlpatterns = [
    path('applications/', VolunteerApplicationView.as_view(), name='volunteer-applications'),
    path('applications/<int:pk>/', VolunteerApplicationView.as_view(), name='volunteer-applications-detail'),

    path('profiles/', VolunteerProfileView.as_view(), name='volunteer-profiles'),

    path('schedules/', VolunteerScheduleView.as_view(), name='volunteer-schedules'),

    path("volunteer/activities/", VolunteerActivityView.as_view(), name="volunteer-activity-crud"),

]