import logging
import stripe
import paypalrestsdk
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from animals.models import Donation
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

from animals.utils import send_email_func

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
        send_email_func(
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
def process_stripe_donation(request):
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
        send_email_func(
            to_email=request.user.email,
            subject="Donation Received",
            message=f"Thank you for donating ${amount} to our shelter!",
        )

        return Response({"client_secret": payment_intent.client_secret, "donation_id": donation.id}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)