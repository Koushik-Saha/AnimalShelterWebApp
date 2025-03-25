from rest_framework import serializers
from .models import MedicalRecord, HealthStatusUpdate


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

class HealthStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthStatusUpdate
        fields = '__all__'
        read_only_fields = ['updated_by', 'updated_at']