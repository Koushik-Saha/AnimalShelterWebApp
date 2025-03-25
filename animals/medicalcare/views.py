from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MedicalRecord, HealthStatusUpdate
from .permissions import IsStaffOrReadOnly
from .serializers import MedicalRecordSerializer, HealthStatusUpdateSerializer


class MedicalRecordCreateView(generics.CreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

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

class MedicalRecordListView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

class MedicalRecordDetailView(generics.RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

class MedicalRecordUpdateView(generics.UpdateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

class MedicalRecordDeleteView(generics.DestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

class HealthStatusUpdateCreateView(generics.CreateAPIView):
    queryset = HealthStatusUpdate.objects.all()
    serializer_class = HealthStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

class HealthStatusUpdateListView(generics.ListAPIView):
    serializer_class = HealthStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthStatusUpdate.objects.filter(animal_id=self.kwargs['animal_id'])