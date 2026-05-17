from django.core.exceptions import ValidationError


def validate_uppercase(value):
    if value.isupper():
        return value
    raise ValidationError("Text must be uppercase")