from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LostPetReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lost_pet_reports")
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    description = models.TextField()
    last_seen_location = models.CharField(max_length=255)
    last_seen_date = models.DateField()
    photo = models.ImageField(upload_to="lostpets/photos/", null=True, blank=True)
    contact_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pet_name} - {self.reporter}"