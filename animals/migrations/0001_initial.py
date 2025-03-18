# Generated by Django 5.1.7 on 2025-03-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Animal",
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
                ("name", models.CharField(max_length=100)),
                ("species", models.CharField(max_length=50)),
                ("breed", models.CharField(blank=True, max_length=100, null=True)),
                ("age", models.IntegerField()),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="animal_images/"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("available", "Available for Adoption"),
                            ("adopted", "Adopted"),
                            ("pending", "Pending Adoption"),
                        ],
                        default="available",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
