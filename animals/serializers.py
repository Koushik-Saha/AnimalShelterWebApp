from rest_framework import serializers
from .models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

    def validate_age(self, value):
        """Ensure age is positive"""
        if value < 0:
            raise serializers.ValidationError("Age must be a positive number.")
        return value

    def validate_name(self, value):
        """Ensure name is at least 2 characters"""
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value