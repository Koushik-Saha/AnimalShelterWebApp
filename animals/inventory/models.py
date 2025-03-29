from django.db import models
from django.conf import settings

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity}) at {self.location}"


class LowStockAlert(models.Model):
    inventory_item = models.ForeignKey("animals.InventoryItem", on_delete=models.CASCADE, related_name="low_stock_alerts")
    quantity = models.PositiveIntegerField()
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inventory_item.name} - {self.message}"
