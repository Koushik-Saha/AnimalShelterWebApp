from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import FosterApplication
from .serializers import FosterApplicationSerializer

class FosterApplicationCreateView(generics.CreateAPIView):
    queryset = FosterApplication.objects.all().order_by('-id')
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FosterApplicationListView(generics.ListAPIView):
    queryset = FosterApplication.objects.all().order_by('-id')
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationDetailView(generics.RetrieveAPIView):
    queryset = FosterApplication.objects.all().order_by('-id')
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationUpdateView(generics.UpdateAPIView):
    queryset = FosterApplication.objects.all().order_by('-id')
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationDeleteView(generics.DestroyAPIView):
    queryset = FosterApplication.objects.all().order_by('-id')
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]