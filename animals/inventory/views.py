from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, LowStockAlert, Order
from .serializers import InventoryItemSerializer, LowStockAlertSerializer, OrderSerializer


class InventoryItemView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all().order_by('-created_at')
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['name', 'category', 'location']
    ordering_fields = ['created_at', 'quantity']


class LowStockAlertView(generics.ListCreateAPIView,
                        generics.RetrieveUpdateDestroyAPIView):
    queryset = LowStockAlert.objects.all().order_by('-created_at')
    serializer_class = LowStockAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['inventory_item', 'notified']
    search_fields = ['message']


class OrderView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'supplier']
    search_fields = ['supplier']
    ordering_fields = ['order_date', 'total_price']