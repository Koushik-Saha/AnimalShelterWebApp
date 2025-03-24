import logging
import stripe
import paypalrestsdk
from django.core.cache import cache
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from . import models
from .models import Animal, AdoptionRequest, Profile, CustomUser, FinancialReport, Notification, Subscription
from .serializers import AnimalSerializer, ProfileSerializer, AdoptionHistorySerializer, FinancialReportSerializer, \
    NotificationSerializer, DonationSerializer, UserDetailSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, filters
from .permissions import IsAdminOrReadOnly, IsUser, IsStaff, IsAdmin
from .models import Donation
from django.conf import settings
from .utils import send_email, send_adoption_email, send_donation_receipt
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from .serializers import AdoptionRequestSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

User = settings.AUTH_USER_MODEL


@api_view(["POST"])
@permission_classes([IsAuthenticated])  # Require authentication
def send_email(request):
    """Send an email notification"""
    subject = request.data.get("subject", "Default Subject")
    message = request.data.get("message", "Default Message")
    recipient = request.data.get("recipient")

    if not recipient:
        return Response({"error": "Recipient email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Sender email from settings.py
            [recipient],  # Recipient email
            fail_silently=False,
        )
        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paypal_payment(request):
    try:
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required"}, status=400)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{"amount": {"total": str(amount), "currency": "USD"}}],
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/api/paypal/success/",
                "cancel_url": "http://127.0.0.1:8000/api/paypal/cancel/",
            },
        })

        # Send email confirmation
        send_email(
            to_email=request.user.email,
            subject="Donation Received",
            message=f"Thank you for donating ${amount} to our shelter!",
        )

        if payment.create():
            approval_url = payment["links"][1]["href"]
            return Response({"approval_url": approval_url}, status=200)
        else:
            return Response({"error": payment.error}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stripe_payment(request):
    try:
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Amount is required"}, status=400)

        # Convert amount to cents (Stripe uses cents)
        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),
            currency="usd",
            payment_method_types=["card"],
        )

        # Save donation record
        donation = Donation.objects.create(
            user=request.user,
            amount=amount,
            transaction_id=payment_intent.id,
            status="Pending",
        )

        # Send email confirmation
        send_email(
            to_email=request.user.email,
            subject="Donation Received",
            message=f"Thank you for donating ${amount} to our shelter!",
        )

        return Response({"client_secret": payment_intent.client_secret, "donation_id": donation.id}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API to register new users and assign them a role.
    Required: username, email, password
    Optional: role (defaults to 'user')
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'user')

    missing_fields = []
    if not username:
        missing_fields.append("username")
    if not email:
        missing_fields.append("email")
    if not password:
        missing_fields.append("password")

    if missing_fields:
        return Response({
            "error": f"The following field(s) are required: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    # Check for existing user/email
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)

    # Assign role and flags
    try:
        if role == 'staff':
            user.is_staff = True
            group = Group.objects.get(name="Shelter Staff")
        elif role == 'admin':
            user.is_staff = True
            user.is_superuser = True
            group = Group.objects.get(name="Admin")
        else:
            group = Group.objects.get(name="User")
    except Group.DoesNotExist:
        return Response({
            "error": f"Group '{role}' does not exist. Please create the group first."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user.save()
    user.groups.add(group)

    return Response({
        "message": "User registered successfully!",
        "username": user.username,
        "email": user.email,
        "role": role
    }, status=status.HTTP_201_CREATED)

# Login and Get Token
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Endpoint for staff login and token retrieval.
    Only staff users can log in through this endpoint.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    missing_fields = []
    if not username:
        missing_fields.append("username")
    if not password:
        missing_fields.append("password")

    if missing_fields:
        return Response({
            "error": f"The following field(s) are required: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            "error": "Invalid username or password."
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.is_staff:
        return Response({
            "error": "Access denied. Only staff users are allowed to log in here."
        }, status=status.HTTP_403_FORBIDDEN)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "message": "Login successful.",
        "username": user.username,
        "role": user.role if hasattr(user, 'role') else "staff"
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if not request.user.is_superuser:
        return Response({"error": "You do not have permission to view users."}, status=403)

    users = CustomUser.objects.all()
    data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        for user in users
    ]
    return Response(data)

def approve_adoption(request, adoption_id):
    try:
        adoption = AdoptionRequest.objects.get(id=adoption_id, status="Pending")
        adoption.status = "Approved"
        adoption.save()

        # Send Notification
        Notification.objects.create(
            user=adoption.user,
            message=f"Your adoption request for {adoption.animal.name} has been approved!"
        )

        return Response({"message": "Adoption approved and notification sent."}, status=status.HTTP_200_OK)

    except AdoptionRequest.DoesNotExist:
        return Response({"error": "Adoption request not found or already processed."}, status=status.HTTP_404_NOT_FOUND)

def get_cached_donation_total():
    donation_sum = cache.get("total_donations")
    if not donation_sum:
        donation_sum = Donation.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
        cache.set("total_donations", donation_sum, timeout=60 * 5)  # 5 mins
    return donation_sum


# List and Create Animals
class AnimalListCreateView(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'species', 'status']

    def create(self, request, *args, **kwargs):
        # Check if the request contains a list of objects
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete a Single Animal
class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class PublicAnimalListView(generics.ListAPIView):
    queryset = Animal.objects.filter(status="available")
    serializer_class = AnimalSerializer
    permission_classes = [AllowAny]  # No authentication required

class FilteredAnimalListView(generics.ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "species", "breed"]
    filterset_fields = ["status"]

# List all adoption requests (only for staff)
class AdoptionRequestListView(generics.ListAPIView):
    queryset = AdoptionRequest.objects.all().order_by('id')  # or 'id' or any field
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return AdoptionRequest.objects.all()
        return AdoptionRequest.objects.filter(user=self.request.user)

# Create a new adoption request
class AdoptionRequestCreateView(generics.CreateAPIView):
    """
    API view for submitting an adoption request.
    """
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        animal = serializer.validated_data.get('animal')

        # Check if the animal exists
        if not Animal.objects.filter(id=animal.id).exists():
            return Response({"error": "Invalid animal ID. This animal does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the animal is available for adoption
        if animal.status != 'available':
            return Response({"error": "This animal is no longer available for adoption."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already requested adoption for this animal
        if AdoptionRequest.objects.filter(user=user, animal=animal).exists():
            logger.warning(f"User {user.username} attempted duplicate adoption request for {animal.name}.")
            return Response({"error": "You have already requested adoption for this animal."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the adoption request with the logged-in user
        serializer.save(user=user, status="Pending")
        logger.info(f"Adoption Request submitted by {user.username} for {animal.name}.")

        return Response({"message": "Adoption request submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)

# Approve or reject an adoption request (Admin only)
class AdoptionRequestUpdateView(generics.UpdateAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        request = self.get_object()
        if request.status == 'Pending' and self.request.user.is_staff:
            if serializer.validated_data.get('status') == 'Approved':
                request.animal.status = 'adopted'
                request.animal.save()
                send_adoption_email(request.user.email, request.animal.name, status)
        serializer.save()

# Delete an adoption request
class AdoptionRequestDeleteView(generics.DestroyAPIView):
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestSerializer
    permission_classes = [IsAuthenticated]


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class AdoptionHistoryView(generics.ListAPIView):
    serializer_class = AdoptionHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AdoptionRequest.objects.filter(user=self.request.user).order_by('-created_at')

class UploadHomeVerificationView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class AnimalListView(generics.ListAPIView):
    """
    Users can view the list of animals.
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated, IsUser]

class ManageAnimalView(generics.RetrieveUpdateDestroyAPIView):
    """
    Shelter Staff can edit or remove animals.
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated, IsStaff]

class FinancialReportsView(generics.ListAPIView):
    """
    Admins can view financial reports.
    """
    queryset = FinancialReport.objects.all()  # Assuming a model exists for financial reports
    serializer_class = FinancialReportSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)

class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_animals = Animal.objects.count()
        total_adoptions = AdoptionRequest.objects.filter(status="Approved").count()
        total_donations = Donation.objects.aggregate(total=models.Sum("amount"))["total"] or 0

        data = {
            "total_animals": total_animals,
            "total_adoptions": total_adoptions,
            "total_donations": total_donations,
        }
        return Response(data)

class DonationHistoryView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user)


class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        email = user.email
        price_id = request.data.get("price_id")

        # Create a Stripe customer if needed
        customer = stripe.Customer.create(email=email)

        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_id}],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"],
        )

        # Save in database
        Subscription.objects.create(
            user=user,
            stripe_customer_id=customer.id,
            stripe_subscription_id=subscription.id,
            amount=subscription['plan']['amount'] / 100,
            status=subscription['status']
        )

        return Response({
            "subscriptionId": subscription.id,
            "clientSecret": subscription.latest_invoice.payment_intent.client_secret
        })

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError:
            return Response(status=400)

        if event['type'] == 'invoice.paid':
            data = event['data']['object']
            customer_id = data['customer']
            amount_paid = data['amount_paid'] / 100
            transaction_id = data['id']

            # Optional: get email and user if you track Stripe customer <-> User
            customer = stripe.Customer.retrieve(customer_id)
            email = customer['email']

            send_donation_receipt(email, amount_paid, transaction_id)

            # Save in DB
            Donation.objects.create(
                user=None,  # or find from customer.email
                amount=amount_paid,
                transaction_id=transaction_id,
                status='Completed'
            )

        return Response(status=200)