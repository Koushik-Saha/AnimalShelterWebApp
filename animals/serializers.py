from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Animal, AdoptionRequest, Profile, FinancialReport, NotificationList
from django.conf import settings


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = "__all__"

class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = "__all__"

class AdoptionHistorySerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source="animal.name", read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = ['id', 'animal_name', 'status', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


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

class AdoptionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = ['id', 'user', 'animal', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        """
        Ensure that the user hasn't already requested adoption for the same animal.
        """
        user = self.context['request'].user
        animal = data.get('animal')

        if AdoptionRequest.objects.filter(user=user, animal=animal).exists():
            raise serializers.ValidationError({"error": "You have already requested adoption for this animal."})

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationList
        fields = '__all__'


User = settings.AUTH_USER_MODEL

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'is_superuser', 'date_joined']