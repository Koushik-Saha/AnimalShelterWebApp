from rest_framework import generics, permissions
from .serializers import AdoptionApplicationSerializer
from .models import AdoptionApplication

class AdoptionApplicationCreateView(generics.CreateAPIView):
    queryset = AdoptionApplication.objects.all().order_by('-id')
    serializer_class = AdoptionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]