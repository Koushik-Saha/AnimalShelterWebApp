from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import VolunteerApplication, VolunteerProfile, VolunteerSchedule, VolunteerActivity
from .serializers import VolunteerApplicationSerializer, VolunteerProfileSerializer, VolunteerScheduleSerializer, \
    VolunteerActivitySerializer
from ..utils import success_response, error_response

class VolunteerApplicationView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = VolunteerApplication.objects.all().order_by('-id')
    serializer_class = VolunteerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'availability']
    search_fields = ['full_name', 'email', 'phone']

    def list(self, request, *args, **kwargs):
        return success_response("Volunteer applications fetched successfully", super().list(request, *args, **kwargs).data)

    def retrieve(self, request, *args, **kwargs):
        return success_response("Volunteer application details", super().retrieve(request, *args, **kwargs).data)

    def create(self, request, *args, **kwargs):
        try:
            return success_response("Volunteer application submitted", super().create(request, *args, **kwargs).data)
        except Exception as e:
            return error_response(str(e))

    def update(self, request, *args, **kwargs):
        try:
            return success_response("Volunteer application updated", super().update(request, *args, **kwargs).data)
        except Exception as e:
            return error_response(str(e))

    def destroy(self, request, *args, **kwargs):
        return success_response("Volunteer application deleted", super().destroy(request, *args, **kwargs).data)


class VolunteerProfileView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = VolunteerProfile.objects.all().order_by('-id')
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['availability', 'skills']
    search_fields = ['full_name', 'skills']


class VolunteerScheduleView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = VolunteerSchedule.objects.all().order_by('-shift_date')
    serializer_class = VolunteerScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['volunteer', 'shift_date', 'location', 'is_confirmed']
    search_fields = ['task_description', 'location']
    ordering_fields = ['shift_date', 'start_time']

class VolunteerActivityView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = VolunteerActivity.objects.all().order_by('-date')
    serializer_class = VolunteerActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['volunteer', 'date', 'activity_type']
    search_fields = ['activity_type', 'description']