from django.urls import path
from .views import InventoryItemView, LowStockAlertView, OrderView

urlpatterns = [
    path('items/', InventoryItemView.as_view(), name='inventory-items'),
    path('items/<int:pk>/', InventoryItemView.as_view(), name='inventory-item-detail'),

    path('alerts/', LowStockAlertView.as_view(), name='low-stock-alerts'),
    path('alerts/<int:pk>/', LowStockAlertView.as_view(), name='low-stock-alerts-detail'),

    path('orders/', OrderView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order-detail'),

]