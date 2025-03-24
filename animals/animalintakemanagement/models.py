import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AnimalIntake(models.Model):
    SOURCE_CHOICES = [
        ('stray', 'Stray'),
        ('surrender', 'Owner Surrender'),
        ('transfer', 'Transferred'),
        ('rescue', 'Rescue'),
    ]

    SEX_CHOICES = [('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')]

    animal_id = models.CharField(max_length=12, unique=True)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.DecimalField(max_digits=4, decimal_places=1)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    color = models.CharField(max_length=50)
    markings = models.TextField(blank=True, null=True)
    health_status = models.TextField()
    temperament = models.CharField(max_length=100)
    history = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    photo = models.ImageField(upload_to="intakes/photos/", blank=True, null=True)
    video = models.FileField(upload_to="intakes/videos/", blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal_id} - {self.species}"

class AnimalIntake(models.Model):
    animal_id = models.CharField(max_length=20, unique=True, editable=False)
    # ... other existing fields ...

    def save(self, *args, **kwargs):
        if not self.animal_id:
            self.animal_id = f"A-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)