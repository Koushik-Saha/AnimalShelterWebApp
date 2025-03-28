from rest_framework import serializers
from .models import VolunteerApplication, VolunteerProfile, VolunteerSchedule


class VolunteerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerApplication
        fields = '__all__'


class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = '__all__'



class VolunteerScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerSchedule
        fields = '__all__'