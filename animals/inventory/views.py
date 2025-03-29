from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, LowStockAlert
from .serializers import InventoryItemSerializer, LowStockAlertSerializer


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