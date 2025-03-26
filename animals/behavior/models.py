from django.db import models
from django.conf import settings
from animals.models import Animal

class BehaviorAssessment(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='behavior_assessments')
    observer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    observed_date = models.DateField()
    temperament = models.CharField(max_length=100)
    interaction_notes = models.TextField()
    behavior_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment for {self.animal.animal_id} on {self.observed_date}"

class EnrichmentActivity(models.Model):
    ACTIVITY_TYPES = [
        ('toy', 'Toy'),
        ('puzzle', 'Puzzle'),
        ('walk', 'Walk'),
        ('training', 'Training'),
        ('other', 'Other'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='enrichment_activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField()
    date_provided = models.DateField()
    effectiveness_rating = models.IntegerField(default=0)
    staff_notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal.name} - {self.activity_type} on {self.date_provided}"


class TrainingNote(models.Model):
    animal = models.ForeignKey('animals.Animal', on_delete=models.CASCADE, related_name='training_notes')
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Training note for {self.animal.name}"