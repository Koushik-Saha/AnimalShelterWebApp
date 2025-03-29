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


class Order(models.Model):
    supplier_name = models.CharField(max_length=100)
    order_date = models.DateField()
    expected_delivery_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")],
        default="pending"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} from {self.supplier_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

