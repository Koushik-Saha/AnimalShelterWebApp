from rest_framework import generics, permissions
from .models import BehaviorAssessment
from .serializers import BehaviorAssessmentSerializer
from .permissions import CanManageBehaviorAssessment

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