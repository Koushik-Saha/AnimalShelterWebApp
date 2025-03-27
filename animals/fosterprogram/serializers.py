from rest_framework import serializers
from .models import FosterApplication

class FosterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterApplication
        fields = '__all__'
        read_only_fields = ['user', 'submitted_at']