from rest_framework import serializers
from .models import LostPetReport

class LostPetReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostPetReport
        fields = '__all__'
        read_only_fields = ["id", "created_at"]