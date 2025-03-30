from rest_framework import serializers
from .models import LostPetReport, FoundAnimalReport, OwnerContactInfo


class LostPetReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostPetReport
        fields = '__all__'
        read_only_fields = ["id", "created_at"]

class FoundAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundAnimalReport
        fields = '__all__'
        read_only_fields = ('id', 'finder', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['finder'] = self.context['request'].user
        return super().create(validated_data)

class OwnerContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerContactInfo
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

