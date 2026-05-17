from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.core.exceptions import ValidationError

class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)

        if isinstance(value, str):
            return value.upper()

        return value


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 13
        super().__init__(*args, **kwargs)

        self.pattern = re.compile(r"^\+380\d{9}$")

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        if value and not self.pattern.match(value):
            raise ValidationError(
                "Phone must be in format +380XXXXXXXXX"
            )

    def get_prep_value(self, value):
        if value is None:
            return value

        value = str(value).strip()

        if not self.pattern.match(value):
            raise ValidationError("Invalid phone format")

        return value


class Product(models.Model):
    name = UpperCaseCharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}: {self.price}$"

    def get_total_value(self):
        return self.quantity * self.price


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()

