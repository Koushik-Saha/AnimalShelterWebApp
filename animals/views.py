import stripe
import paypalrestsdk
from .models import Animal
from .serializers import AnimalSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, filters
from .permissions import IsAdminOrReadOnly
from .models import Donation
from django.conf import settings
from .utils import send_email
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail




stripe.api_key = settings.STRIPE_SECRET_KEY


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



# Register a New Staff Member
@api_view(['POST'])
@permission_classes([AllowAny])
def register_staff(request):
    """Endpoint to register a staff user"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user.is_staff = True  # Mark as staff
    user.save()

    token, created = Token.objects.get_or_create(user=user)
    return Response({"message": "Staff registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)


# Login and Get Token
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Endpoint for staff login and token retrieval"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None or not user.is_staff:
        return Response({"error": "Invalid credentials or not a staff user."}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_200_OK)

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