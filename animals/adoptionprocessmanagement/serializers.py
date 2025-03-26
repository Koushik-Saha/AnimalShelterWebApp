from rest_framework import serializers
from .models import AdoptionApplication, MatchingTool


class AdoptionApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionApplication
        fields = '__all__'
        read_only_fields = ('id', 'user', 'submitted_at')

    def validate(self, data):
        # Example: Add any additional validation if needed
        if data.get('own_or_rent') == 'rent' and not data.get('landlord_permission'):
            raise serializers.ValidationError("Landlord permission is required if renting.")
        return data

class AdoptionApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionApplication
        fields = ['id', 'status', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class MatchingToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingTool
        fields = '__all__'
        read_only_fields = ['adopter', 'created_at']
