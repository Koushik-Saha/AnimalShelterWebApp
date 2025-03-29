from rest_framework import serializers
from .models import InventoryItem, LowStockAlert


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class LowStockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = LowStockAlert
        fields = '__all__'