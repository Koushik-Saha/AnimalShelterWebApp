from rest_framework import serializers
from .models import BehaviorAssessment

class BehaviorAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorAssessment
        fields = '__all__'
        read_only_fields = ['observer', 'created_at']