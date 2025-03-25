# Generated by Django 5.1.7 on 2025-03-25 03:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0005_animalintake_age_animalintake_breed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="animalintake",
            name="stay_history",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.CreateModel(
            name="MedicalRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("animal_id", models.CharField(max_length=20)),
                (
                    "vaccination",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("rabies", "Rabies"),
                            ("distemper", "Distemper"),
                            ("parvo", "Parvovirus"),
                            ("bordetella", "Bordetella"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("deworming_date", models.DateField(blank=True, null=True)),
                ("flea_tick_treatment_date", models.DateField(blank=True, null=True)),
                ("medical_history", models.TextField(blank=True, null=True)),
                ("diagnosis", models.TextField(blank=True, null=True)),
                ("treatment", models.TextField(blank=True, null=True)),
                ("medication", models.TextField(blank=True, null=True)),
                ("vet_notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
