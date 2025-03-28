# animals/volunteer/models.py
from django.db import models
from django.contrib.auth import get_user_model

from animal_shelter import settings

User = get_user_model()

class VolunteerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_applications")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    availability = models.CharField(max_length=100)  # e.g. Weekends, Weekdays, Evenings
    interests = models.TextField(help_text="What areas are you interested in volunteering for?")
    experience = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer_profile")
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    skills = models.TextField()
    availability = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Volunteer Profile"


class VolunteerSchedule(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_schedules")
    shift_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    task_description = models.TextField()
    location = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.volunteer.username} - {self.shift_date} ({self.start_time} to {self.end_time})"

class VolunteerActivity(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer} - {self.activity_type} on {self.date}"

class VolunteerMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

