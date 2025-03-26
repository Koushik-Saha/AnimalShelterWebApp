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