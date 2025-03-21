from django.core.mail import send_mail
from django.conf import settings


def send_donation_email(user_email, amount):
    send_mail(
        "Thank You for Your Donation!",
        f"Dear supporter,\n\nThank you for your generous donation of ${amount}. Your support helps us rescue and care for more animals.\n\nBest regards,\nAnimal Shelter Team",
        "your-email@gmail.com",
        [user_email],
        fail_silently=False,
    )

def send_email(to_email, subject, message):
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