from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentListView,
    AppointmentDetailView,
    AppointmentUpdateView,
    AppointmentDeleteView
)

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
]