from rest_framework import serializers
from .models import BehaviorAssessment, EnrichmentActivity, TrainingNote


class BehaviorAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorAssessment
        fields = '__all__'
        read_only_fields = ['observer', 'created_at']

class EnrichmentActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrichmentActivity
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at']

class TrainingNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingNote
        fields = '__all__'