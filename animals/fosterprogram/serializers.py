from rest_framework import serializers
from .models import FosterApplication, FosterPlacement
from ..models import Animal


class FosterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterApplication
        fields = '__all__'
        read_only_fields = ['user', 'submitted_at']

class MatchedFosterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterApplication
        fields = '__all__'

class MatchedAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class FosterPlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FosterPlacement
        fields = '__all__'