from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import AdoptionApplicationSerializer
from .models import AdoptionApplication
from ..permissions import IsAdminOrShelterStaff
from rest_framework.response import Response
from rest_framework import status




class AdoptionApplicationCreateView(generics.CreateAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdoptionApplicationListView(generics.ListAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]


class AdoptionApplicationDetailView(generics.RetrieveAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]


class AdoptionApplicationUpdateView(generics.UpdateAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrShelterStaff]

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if application.status != "Pending":
            return Response(
                {"error": "This application has already been processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_status = request.data.get("status")
        if new_status not in ["Approved", "Rejected"]:
            return Response(
                {"error": "Invalid status. Must be 'Approved' or 'Rejected'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = new_status
        application.reviewed_by = request.user
        application.save()

        return Response(
            {
                "message": f"Application status updated to {new_status}",
                "application_id": application.id,
                "status": new_status,
            },
            status=status.HTTP_200_OK,
        )