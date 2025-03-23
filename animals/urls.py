from django.urls import path

from .admins.admin_views import AdminCustomReportView
from .analytics.analytics_views import AdoptionSuccessAnalyticsView, DonationTrendAnalyticsView, DonationCSVExportView
from .ml.ml_views import AnimalMatchSuggestionView
from .views import AnimalListCreateView, AnimalDetailView, PublicAnimalListView, FilteredAnimalListView, send_email, \
    AdoptionRequestListView, AdoptionRequestCreateView, AdoptionRequestUpdateView, AdoptionRequestDeleteView, \
    UserProfileView, AdoptionHistoryView, UploadHomeVerificationView, FinancialReportsView, AnimalListView, \
    ManageAnimalView, NotificationListView, approve_adoption, AdminDashboardView, DonationHistoryView, \
    CreateSubscriptionView, StripeWebhookView
from .views import register_user, login_user
from .views import create_stripe_payment, create_paypal_payment
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # Login & Register
    path('register/', register_user, name='register_staff'),
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
    # Upload home verification
    path('upload-home-verification/', UploadHomeVerificationView.as_view(), name='upload-home-verification'),
    # Animals view manage role
    path('animals/', AnimalListView.as_view(), name='list-animals'),
    path('manage-animal/<int:pk>/', ManageAnimalView.as_view(), name='manage-animal'),
    path('financial-reports/', FinancialReportsView.as_view(), name='financial-reports'),
    # Notification system
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('approve-adoption/<int:adoption_id>/', approve_adoption, name='approve_adoption'),
    #admin dashboard details
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    # Donation history
    path('donation-history/', DonationHistoryView.as_view(), name='donation-history'),
    # Subscription for monthly
    path('subscribe/', CreateSubscriptionView.as_view(), name='create-subscription'),
    # Add Webhook Endpoint
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
    # JWT Token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Adoption success analytics
    path("analytics/adoption-success/", AdoptionSuccessAnalyticsView.as_view(), name="adoption-success-analytics"),
    # Donation trend analytics
    path("analytics/donations/", DonationTrendAnalyticsView.as_view(), name="donation-trend-analytics"),
    # Donation CSV export
    path("analytics/donations/export/", DonationCSVExportView.as_view(), name="donation-csv-export"),
    # Admin custom report
    path("analytics/custom-report/", AdminCustomReportView.as_view(), name="custom-report"),
    # Animal Match Suggestion
    path("match-animals/", AnimalMatchSuggestionView.as_view(), name="animal-match"),

]