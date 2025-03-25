from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer

class MedicalRecordCreateView(generics.CreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Medical record created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)