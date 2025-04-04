from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FosterApplication, FosterPlacement, FosterCommunication
from .serializers import FosterApplicationSerializer, MatchedFosterApplicationSerializer, MatchedAnimalSerializer, \
    FosterPlacementSerializer, FosterCommunicationSerializer
from django.db.models import Q
from ..models import Animal


class FosterApplicationCreateView(generics.CreateAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FosterApplicationListView(generics.ListAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationDetailView(generics.RetrieveAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationUpdateView(generics.UpdateAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterApplicationDeleteView(generics.DestroyAPIView):
    queryset = FosterApplication.objects.all()
    serializer_class = FosterApplicationSerializer
    permission_classes = [IsAdminUser]

class FosterMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # You can add real logic here based on attributes like experience, yard, special needs, etc.
        matched_pairs = []

        foster_apps = FosterApplication.objects.all()
        animals = Animal.objects.all()

        for foster in foster_apps:
            matched = animals.filter(
                temperament__icontains="calm",
                health_status__icontains="healthy"
            )
            for animal in matched:
                matched_pairs.append({
                    "foster_application": MatchedFosterApplicationSerializer(foster).data,
                    "matched_animal": MatchedAnimalSerializer(animal).data,
                })

        return Response(matched_pairs)

class FosterPlacementListCreateView(generics.ListCreateAPIView):
    queryset = FosterPlacement.objects.all()
    serializer_class = FosterPlacementSerializer
    permission_classes = [IsAuthenticated]

class FosterPlacementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FosterPlacement.objects.all()
    serializer_class = FosterPlacementSerializer
    permission_classes = [IsAuthenticated]

class FosterCommunicationCreateView(generics.CreateAPIView):
    queryset = FosterCommunication.objects.all()
    serializer_class = FosterCommunicationSerializer
    permission_classes = [IsAuthenticated]

class FosterCommunicationListView(generics.ListAPIView):
    serializer_class = FosterCommunicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FosterCommunication.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).order_by("-sent_at")