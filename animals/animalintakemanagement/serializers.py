from rest_framework import serializers
from .models import AnimalIntake
from .validators import validate_age


class AnimalIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalIntake
        exclude = ['created_by']

    def validate_age(self, value):
        return validate_age(value)