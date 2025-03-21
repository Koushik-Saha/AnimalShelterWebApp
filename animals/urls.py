from django.urls import path
from .views import AnimalListCreateView, AnimalDetailView, PublicAnimalListView, FilteredAnimalListView, send_email, \
    AdoptionRequestListView, AdoptionRequestCreateView, AdoptionRequestUpdateView, AdoptionRequestDeleteView, \
    UserProfileView, AdoptionHistoryView
from .views import register_staff, login_user
from .views import create_stripe_payment, create_paypal_payment


urlpatterns = [
    # Login & Register
    path('register/', register_staff, name='register_staff'),
    path('login/', login_user, name='login_user'),
    # Animal CRUD
    path('animals/', AnimalListCreateView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
    # Payment
    path("stripe-payment/", create_stripe_payment, name="stripe-payment"),
    path("paypal-payment/", create_paypal_payment, name="paypal-payment"),
    # Animal Public
    path('public-animals/', PublicAnimalListView.as_view(), name='public-animals'),
    path('animals/', FilteredAnimalListView.as_view(), name='filtered-animals'),
    # Email
    path("email/", send_email, name="send-email"),
    # Animal adoption route
    path('adopt/', AdoptionRequestCreateView.as_view(), name='adopt-animal'),
    path('adopt/requests/', AdoptionRequestListView.as_view(), name='adoption-requests'),
    path('adopt/requests/<int:pk>/', AdoptionRequestUpdateView.as_view(), name='update-adoption'),
    path('adopt/requests/<int:pk>/delete/', AdoptionRequestDeleteView.as_view(), name='delete-adoption'),
    # Update profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    # Adoption History
    path('adoption-history/', AdoptionHistoryView.as_view(), name='adoption-history'),

]