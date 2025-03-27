from django.db import models
from django.conf import settings

from animals.models import Animal


class FosterApplication(models.Model):


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    has_other_pets = models.BooleanField()
    pet_experience = models.TextField()
    has_children = models.BooleanField()
    home_type = models.CharField(max_length=100)
    fenced_yard = models.BooleanField()
    foster_duration_preference = models.CharField(max_length=100)
    reason_for_fostering = models.TextField()
    availability_start = models.DateField()
    availability_end = models.DateField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.full_name} - Foster Application"


class FosterPlacement(models.Model):
    foster_application = models.ForeignKey(FosterApplication, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="active")  # active, completed, etc.

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.name} placed with {self.foster_application.full_name}"

class FosterCommunication(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    foster_application = models.ForeignKey("FosterApplication", on_delete=models.CASCADE, related_name="communications")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"