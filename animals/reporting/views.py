from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .models import Report
from .serializers import ReportSerializer
from ..medicalcare.models import MedicalRecord
from ..models import Animal, AdoptionRequest, Donation
from ..permissions import IsAdminOrStaff
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from ..volunteer.models import VolunteerActivity


class ReportView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'created_by']
    search_fields = ['title']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


class DashboardKPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        today = datetime.today()
        last_30_days = today - timedelta(days=30)

        data = {
            "animal_intake": Animal.objects.filter(intake_date__gte=last_30_days).count(),
            "adoptions": AdoptionRequest.objects.filter(date__gte=last_30_days).count(),
            "medical_treatments": MedicalRecord.objects.filter(date__gte=last_30_days).count(),
            "volunteer_hours": VolunteerActivity.objects.filter(date__gte=last_30_days).aggregate(total_hours=Sum("hours"))['total_hours'] or 0,
            "donations_received": Donation.objects.filter(date__gte=last_30_days).aggregate(total=Sum("amount"))['total'] or 0,
        }

        return Response({"success": True, "message": "KPI Data", "data": data})