from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django_recaptcha.fields import ReCaptchaField

class CaptchaPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField()