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

    species = models.CharField(max_length=50, null=True, blank=True)
    breed = models.CharField(max_length=50, null=True, blank=True)
    age = models.FloatField(default=0.0)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    markings = models.TextField(blank=True, null=True)
    health_status = models.TextField(null=True, blank=True)
    temperament = models.CharField(max_length=100, null=True, blank=True)
    history = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, null=True, blank=True)
    photo = models.ImageField(upload_to="intakes/photos/", blank=True, null=True)
    video = models.FileField(upload_to="intakes/videos/", blank=True, null=True)
    animal_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)

    # animal_id = models.CharField(max_length=12, unique=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    photos = models.ImageField(upload_to='animal_photos/', null=True, blank=True)
    videos = models.FileField(upload_to='animal_videos/', null=True, blank=True)

    stay_history = models.JSONField(default=list, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.animal_id:
            self.animal_id = f"A-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)