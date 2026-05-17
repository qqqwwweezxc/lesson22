from django.core.exceptions import ValidationError


def validate_uppercase(value):
    """Checks if the value is a valid uppercase string"""
    if value.isupper():
        return value
    raise ValidationError("Text must be uppercase")