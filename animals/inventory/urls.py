from django.urls import path
from .views import InventoryItemView, LowStockAlertView

urlpatterns = [
    path('items/', InventoryItemView.as_view(), name='inventory-items'),
    path('items/<int:pk>/', InventoryItemView.as_view(), name='inventory-item-detail'),

    path('alerts/', LowStockAlertView.as_view(), name='low-stock-alerts'),
    path('alerts/<int:pk>/', LowStockAlertView.as_view(), name='low-stock-alerts-detail'),

]