from rest_framework import serializers
from .models import VolunteerApplication, VolunteerProfile, VolunteerSchedule, VolunteerActivity


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

class VolunteerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerActivity
        fields = "__all__"