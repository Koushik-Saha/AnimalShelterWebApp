from django.db import models
from django.conf import settings

class FosterApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    has_other_pets = models.BooleanField()
    pet_experience = models.TextField()
    has_children = models.BooleanField()
    home_type = models.CharField(max_length=100)  # apartment, house, etc.
    fenced_yard = models.BooleanField()
    foster_duration_preference = models.CharField(max_length=100)
    reason_for_fostering = models.TextField()
    availability_start = models.DateField()
    availability_end = models.DateField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - Foster Application"