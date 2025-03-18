from django.db import models

class Animal(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending Adoption'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)  # e.g., Dog, Cat, Rabbit
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='animal_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.species}) - {self.get_status_display()}"