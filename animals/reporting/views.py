from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Report
from .serializers import ReportSerializer

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