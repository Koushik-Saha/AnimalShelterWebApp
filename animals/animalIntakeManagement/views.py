from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AnimalIntake
from .serializers import AnimalIntakeSerializer
from .permissions import IsStaffOrAdmin

class AnimalIntakeCreateView(generics.CreateAPIView):
    queryset = AnimalIntake.objects.all()
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

    def perform_create(self, serializer):
        animal = serializer.save(created_by=self.request.user)
        return Response({
            "message": "Animal intake recorded successfully.",
            "animal_id": animal.animal_id
        }, status=status.HTTP_201_CREATED)