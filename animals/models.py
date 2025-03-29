from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .inventory.models import InventoryItem
from .reporting.models import Report

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    adopted_animals = models.ManyToManyField("Animal", blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    home_verification_document = models.FileField(upload_to='home_verifications/', blank=True, null=True)

    adoption_success_count = models.IntegerField(default=0)  # ✅
    home_type = models.CharField(max_length=100, blank=True)  # Apartment, House
    pet_experience = models.BooleanField(default=False)
    has_yard = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('staff', 'Shelter Staff'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Donation(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_COMPLETED = "Completed"
    STATUS_CHOICES = [(STATUS_PENDING, "Pending"), (STATUS_COMPLETED, "Completed")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} - {self.amount} USD"



class Animal(models.Model):
    STATUS_CHOICES = [
        ('available', _('Available for Adoption')),
        ('adopted', _('Adopted')),
        ('pending', _('Pending Adoption')),
    ]

    FRIENDLY = 'Friendly'
    AGGRESSIVE = 'Aggressive'
    SHY = 'Shy'
    PLAYFUL = 'Playful'

    TEMPERAMENT_CHOICES = [
        (FRIENDLY, 'Friendly'),
        (AGGRESSIVE, 'Aggressive'),
        (SHY, 'Shy'),
        (PLAYFUL, 'Playful'),
    ]

    HEALTH_STATUS_CHOICES = [
        ("healthy", "Healthy"),
        ("needs_care", "Needs Care"),
        ("critical", "Critical"),
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
    temperament = models.CharField(max_length=50, choices=TEMPERAMENT_CHOICES, default=FRIENDLY)

    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_STATUS_CHOICES,
        default="healthy",
    )

    def __str__(self):
        return f"{self.name} ({self.species}) - {self.get_status_display()}"

class AdoptionRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.animal.name} ({self.status})"

class AnimalImage(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="animal_images/")

    def __str__(self):
        return f"Image for {self.animal.name}"


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """
    Ensures default roles (User, Staff, Admin) and permissions exist after migrations.
    """
    if sender.name != "animals":
        return  # Ensure this only runs for the 'animals' app

    print("Creating default roles and permissions...")

    # Define roles
    roles = {
        "User": [],
        "Shelter Staff": ["add_animal", "change_animal", "delete_animal", "view_animal"],
        "Admin": ["add_animal", "change_animal", "delete_animal", "view_animal", "view_financialreport"],
    }

    # Create groups and assign permissions
    for role_name, permissions in roles.items():
        group, created = Group.objects.get_or_create(name=role_name)
        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"⚠️ Warning: Permission '{perm}' does not exist yet.")

    print("✅ Default roles and permissions created successfully.")

class FinancialReport(models.Model):
    """
    Model to store financial reports for the animal shelter.
    Only admins should have access to this data.
    """
    title = models.CharField(max_length=255)
    report_date = models.DateField(auto_now_add=True)
    total_donations = models.DecimalField(max_digits=12, decimal_places=2)
    expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.report_date}"

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

class NotificationList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NotificationList for {self.user.username}: {self.message}"