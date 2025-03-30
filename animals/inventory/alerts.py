from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import InventoryItem
from django.conf import settings

LOW_STOCK_THRESHOLD = 10  # Example threshold

@receiver(post_save, sender=InventoryItem)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity <= LOW_STOCK_THRESHOLD:
        send_mail(
            subject=f"Low Stock Alert: {instance.name}",
            message=f"Item '{instance.name}' is low in stock. Quantity remaining: {instance.quantity} at {instance.location}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
        )
