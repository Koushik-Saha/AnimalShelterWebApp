from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas

from animals.models import Animal


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

    agreement_text = models.TextField(blank=True, null=True)
    agreement_pdf = models.FileField(upload_to="adoption_agreements/", blank=True, null=True)

    def __str__(self):
        return f"Adoption Application by {self.full_name}"

    def generate_agreement_pdf(self):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Adoption Agreement for: {self.full_name}")
        p.drawString(100, 780, f"Address: {self.address}")
        p.drawString(100, 760, f"Phone: {self.phone_number}")
        p.drawString(100, 740, f"Email: {self.email}")
        p.drawString(100, 720, f"Commitment: {self.lifelong_care_commitment}")
        p.drawString(100, 700, "Thank you for choosing to adopt!")
        p.showPage()
        p.save()

        buffer.seek(0)
        return ContentFile(buffer.read(), name=f"{self.full_name}_agreement.pdf")


class MatchingTool(models.Model):
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=50)
    activity_level = models.CharField(max_length=50)
    home_environment = models.CharField(max_length=100)
    has_children = models.BooleanField()
    has_other_pets = models.BooleanField()
    allergies = models.BooleanField(default=False)
    preferred_size = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adopter.username} - {self.pet_type} Preference"

class AdoptionAgreement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    agreement_text = models.TextField()
    pdf_file = models.FileField(upload_to='agreements/pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agreement for {self.user.username} - {self.animal.name}"

    def generate_pdf(self):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Adoption Agreement")
        p.drawString(100, 780, f"User: {self.user.username}")
        p.drawString(100, 760, f"Animal: {self.animal.name}")
        text_object = p.beginText(100, 740)
        for line in self.agreement_text.splitlines():
            text_object.textLine(line)
        p.drawText(text_object)
        p.showPage()
        p.save()

        buffer.seek(0)
        self.pdf_file.save(f"agreement_{self.user.id}_{self.animal.id}.pdf", ContentFile(buffer.read()), save=False)
        buffer.close()
