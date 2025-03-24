from rest_framework import serializers
from .models import AnimalIntake
from .validators import validate_age


class AnimalIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalIntake
        fields = '__all__'
        read_only_fields = ['animal_id']

    def validate(self, data):
        if not data.get("animal_id"):
            raise serializers.ValidationError({"animal_id": "Animal ID is required."})
        if not data.get("source"):
            raise serializers.ValidationError({"source": "Please provide a valid source of intake."})
        return data