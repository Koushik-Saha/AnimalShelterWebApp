from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    adopted_animals = models.ManyToManyField("Animal", blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    home_verification_document = models.FileField(upload_to='home_verifications/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CustomUser(AbstractUser):
    """
    Custom user model with roles.
    """
    ROLE_CHOICES = [
        ('user', 'User'),         # 🏠 Can view animals, request adoptions, donate
        ('staff', 'Shelter Staff'),  # 👩‍⚕️ Can manage animals, approve adoptions
        ('admin', 'Admin'),       # 🏛 Full access, financial reports
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"


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
    Automatically creates default user roles with permissions.
    """
    if sender.name == "animals":  # Replace with your app name
        user_group, _ = Group.objects.get_or_create(name="User")
        staff_group, _ = Group.objects.get_or_create(name="Shelter Staff")
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        # Assign permissions
        user_permissions = ['view_animal', 'add_adoptionrequest']
        staff_permissions = ['add_animal', 'change_animal', 'delete_animal', 'change_adoptionrequest']
        admin_permissions = ['add_animal', 'change_animal', 'delete_animal', 'change_adoptionrequest', 'view_financial_reports']

        for perm in user_permissions:
            permission = Permission.objects.get(codename=perm)
            user_group.permissions.add(permission)

        for perm in staff_permissions:
            permission = Permission.objects.get(codename=perm)
            staff_group.permissions.add(permission)

        for perm in admin_permissions:
            permission = Permission.objects.get(codename=perm)
            admin_group.permissions.add(permission)