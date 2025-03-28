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
    name = models.CharField(max_length=100, default="Unnamed")
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("resolved", "Resolved")],
        default="pending"
    )

    def __str__(self):
        return f"{self.pet_name} - {self.reporter}"


class FoundAnimalReport(models.Model):
    finder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="found_animal_reports")
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    description = models.TextField()
    found_location = models.CharField(max_length=255)
    found_date = models.DateField()
    photo = models.ImageField(upload_to="foundanimals/photos/", null=True, blank=True)
    contact_info = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[("under_review", "Under Review"), ("available", "Available"), ("claimed", "Claimed")],
        default="under_review"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.species} reported by {self.finder}"
