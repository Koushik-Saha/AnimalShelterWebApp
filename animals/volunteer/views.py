from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import VolunteerApplication
from .serializers import VolunteerApplicationSerializer
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