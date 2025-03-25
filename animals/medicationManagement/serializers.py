from rest_framework import serializers
from .models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ['created_at', 'administered_by']

    def create(self, validated_data):
        validated_data['administered_by'] = self.context['request'].user
        return super().create(validated_data)