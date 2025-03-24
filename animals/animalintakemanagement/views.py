from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AnimalIntakeSerializer

class AnimalIntakeCreateView(generics.CreateAPIView):
    serializer_class = AnimalIntakeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "Animal intake created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)