from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .models import BehaviorAssessment, EnrichmentActivity, TrainingNote
from .serializers import BehaviorAssessmentSerializer, EnrichmentActivitySerializer, TrainingNoteSerializer
from .permissions import CanManageBehaviorAssessment, IsStaffOrReadOnly


class CreateBehaviorAssessmentView(generics.CreateAPIView):
    queryset = BehaviorAssessment.objects.all()
    serializer_class = BehaviorAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageBehaviorAssessment]

    def perform_create(self, serializer):
        serializer.save(observer=self.request.user)

class ListBehaviorAssessmentsView(generics.ListAPIView):
    serializer_class = BehaviorAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BehaviorAssessment.objects.filter(animal__id=self.kwargs["animal_id"])

class BehaviorAssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BehaviorAssessment.objects.all()
    serializer_class = BehaviorAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageBehaviorAssessment]


class EnrichmentActivityCreateView(generics.CreateAPIView):
    serializer_class = EnrichmentActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EnrichmentActivityListView(generics.ListAPIView):
    serializer_class = EnrichmentActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EnrichmentActivity.objects.all()

class TrainingNoteCreateView(generics.CreateAPIView):
    queryset = TrainingNote.objects.all()
    serializer_class = TrainingNoteSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TrainingNoteListView(generics.ListAPIView):
    queryset = TrainingNote.objects.all()
    serializer_class = TrainingNoteSerializer
    permission_classes = [IsAuthenticated]

class TrainingNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainingNote.objects.all()
    serializer_class = TrainingNoteSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]