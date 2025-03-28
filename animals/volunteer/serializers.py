from rest_framework import serializers
from .models import VolunteerApplication, VolunteerProfile, VolunteerSchedule, VolunteerActivity, VolunteerMessage


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


class VolunteerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerMessage
        fields = '__all__'
        read_only_fields = ['sender', 'sent_at']