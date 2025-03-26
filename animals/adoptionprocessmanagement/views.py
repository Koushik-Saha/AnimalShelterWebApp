from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import AdoptionApplicationSerializer
from .models import AdoptionApplication
from ..permissions import IsStaffOrAdmin


class AdoptionApplicationCreateView(generics.CreateAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdoptionApplicationListView(generics.ListAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-created_at')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]


class AdoptionApplicationDetailView(generics.RetrieveAPIView):
    queryset = AdoptionApplication.objects.all()
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]