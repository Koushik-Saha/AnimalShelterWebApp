from django.db import models
from django.conf import settings

class AdoptionApplication(models.Model):
    HOME_TYPES = [
        ("apartment", "Apartment"),
        ("house", "House"),
        ("other", "Other"),
    ]

    PET_TYPES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Applicant Information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    date_of_birth = models.DateField()

    # Household Details
    home_type = models.CharField(max_length=20, choices=HOME_TYPES)
    owns_home = models.BooleanField()
    landlord_permission = models.BooleanField(null=True, blank=True)
    number_of_adults = models.IntegerField()
    number_of_children = models.IntegerField()
    allergies = models.TextField(blank=True, null=True)

    # Lifestyle and Experience
    work_schedule = models.CharField(max_length=100)
    previous_pet_experience = models.TextField()
    current_pets = models.TextField(blank=True, null=True)

    # Animal Preferences
    preferred_pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    preferred_breed_or_size = models.CharField(max_length=100)
    preferred_age_range = models.CharField(max_length=100)
    adoption_reason = models.TextField()

    # Pet Care Plans
    daily_care_plan = models.TextField()
    vacation_care_plan = models.TextField()
    pet_care_budget = models.DecimalField(max_digits=10, decimal_places=2)
    emergency_plan = models.TextField()

    # Commitment and Agreement
    lifelong_care_commitment = models.BooleanField()
    consent_home_visits = models.BooleanField()
    understands_return_policy = models.BooleanField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Adoption Application by {self.full_name}"
