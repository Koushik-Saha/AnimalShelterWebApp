from django.db import models
from django.conf import settings

from animals.models import Animal


class MedicalRecord(models.Model):
    VACCINE_CHOICES = [
        ('Rabies', 'Rabies'),
        ('Distemper', 'Distemper'),
        ('Parvovirus', 'Parvovirus'),
        ('Bordetella', 'Bordetella'),
    ]

    animal_id = models.CharField(max_length=20)
    vaccination = models.CharField(max_length=50, choices=VACCINE_CHOICES, blank=True, null=True)
    deworming_date = models.DateField(blank=True, null=True)
    flea_tick_treatment_date = models.DateField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    vet_notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for {self.animal_id}"


class HealthStatusUpdate(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="health_updates")
    status = models.TextField()
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.animal.name} - {self.status[:30]}"