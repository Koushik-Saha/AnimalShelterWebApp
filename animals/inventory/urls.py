from django.urls import path
from .views import InventoryItemView

urlpatterns = [
    path('items/', InventoryItemView.as_view(), name='inventory-items'),
    path('items/<int:pk>/', InventoryItemView.as_view(), name='inventory-item-detail'),
]