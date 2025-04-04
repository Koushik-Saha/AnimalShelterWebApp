# Generated by Django 5.1.7 on 2025-03-29 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0032_inventoryitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="LowStockAlert",
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
                ("quantity", models.PositiveIntegerField()),
                ("message", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("notified", models.BooleanField(default=False)),
                (
                    "inventory_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="low_stock_alerts",
                        to="animals.inventoryitem",
                    ),
                ),
            ],
        ),
    ]
