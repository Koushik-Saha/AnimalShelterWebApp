from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def send_donation_email(user_email, amount):
    send_mail(
        "Thank You for Your Donation!",
        f"Dear supporter,\n\nThank you for your generous donation of ${amount}. Your support helps us rescue and care for more animals.\n\nBest regards,\nAnimal Shelter Team",
        "your-email@gmail.com",
        [user_email],
        fail_silently=False,
    )

def send_email_func(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

def send_adoption_email(user_email, animal_name, status):
    subject = f"Adoption Request Update: {animal_name}"
    message = f"Your adoption request for {animal_name} has been {status}."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

def send_donation_receipt(user_email, amount, transaction_id):
    subject = 'Thank You for Your Donation!'
    message = (
        f'Dear Donor,\n\n'
        f'Thank you for your generous donation of ${amount}.\n'
        f'Transaction ID: {transaction_id}\n\n'
        f'We appreciate your support!\n\n'
        f'- Animal Shelter Team'
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])


def success_response(data=None, message="Success", code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=code)

def error_response(errors=None, message="Failed", code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "message": message,
        "errors": errors
    }, status=code)