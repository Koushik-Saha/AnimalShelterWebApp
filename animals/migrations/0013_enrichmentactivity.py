# Generated by Django 5.1.7 on 2025-03-26 07:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0012_behaviorassessment"),
    ]

    operations = [
        migrations.CreateModel(
            name="EnrichmentActivity",
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
                (
                    "activity_type",
                    models.CharField(
                        choices=[
                            ("toy", "Toy"),
                            ("puzzle", "Puzzle"),
                            ("walk", "Walk"),
                            ("training", "Training"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("description", models.TextField()),
                ("date_provided", models.DateField()),
                ("effectiveness_rating", models.IntegerField(default=0)),
                ("staff_notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="enrichment_activities",
                        to="animals.animal",
                    ),
                ),
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
