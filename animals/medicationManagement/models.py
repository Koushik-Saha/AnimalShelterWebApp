from django.db import models
from django.conf import settings
from animals.models import Animal

class Medication(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    administration_time = models.DateTimeField()
    administered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    stock_available = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)