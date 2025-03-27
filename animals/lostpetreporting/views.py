from rest_framework import viewsets, permissions
from .models import LostPetReport
from .serializers import LostPetReportSerializer

class LostPetReportViewSet(viewsets.ModelViewSet):
    queryset = LostPetReport.objects.all()
    serializer_class = LostPetReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LostPetReport.objects.all()
        return LostPetReport.objects.filter(reporter=user)