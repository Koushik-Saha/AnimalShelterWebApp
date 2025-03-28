# animals/volunteer/models.py
from django.db import models
from django.contrib.auth import get_user_model

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
