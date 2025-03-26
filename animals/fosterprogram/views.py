from rest_framework import generics, permissions
from .models import FosterApplication
from .serializers import FosterApplicationSerializer
from .permissions import IsUserOrAdmin

class FosterApplicationCreateView(generics.CreateAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)