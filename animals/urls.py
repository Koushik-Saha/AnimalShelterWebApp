from django.urls import path
from .views import AnimalListCreateView, AnimalDetailView, PublicAnimalListView, FilteredAnimalListView
from .views import register_staff, login_user
from .views import create_stripe_payment, create_paypal_payment


urlpatterns = [
    path('register/', register_staff, name='register_staff'),
    path('login/', login_user, name='login_user'),
    path('animals/', AnimalListCreateView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
    path("stripe-payment/", create_stripe_payment, name="stripe-payment"),
    path("paypal-payment/", create_paypal_payment, name="paypal-payment"),
    path('public-animals/', PublicAnimalListView.as_view(), name='public-animals'),
    path('animals/', FilteredAnimalListView.as_view(), name='filtered-animals'),
]