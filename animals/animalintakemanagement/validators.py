from rest_framework.exceptions import ValidationError

def validate_age(value):
    if value < 0 or value > 100:
        raise ValidationError("Age must be between 0 and 100 years.")
    return value