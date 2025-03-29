from django.db import models

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ("intake", "Animal Intake"),
        ("adoption", "Adoption"),
        ("medical", "Medical Treatments"),
        ("volunteer", "Volunteer Hours"),
        ("financial", "Financial Data"),
    ]

    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    parameters = models.JSONField()  # e.g., filters like date range
    generated_file = models.FileField(upload_to="reports/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        'animals.CustomUser',
        on_delete=models.CASCADE,
        related_name="generated_reports"
    )

    def __str__(self):
        return f"{self.title} ({self.report_type})"