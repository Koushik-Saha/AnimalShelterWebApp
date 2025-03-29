from rest_framework import serializers
from .models import InventoryItem, LowStockAlert, OrderItem, Order


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class LowStockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = LowStockAlert
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        instance.items.all().delete()
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)
        return instance