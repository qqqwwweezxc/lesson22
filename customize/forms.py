from django import forms
from .utils import validate_uppercase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class FancySelect(forms.Select):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {})

        attrs.setdefault("class", "form-select shadow")
        attrs.setdefault("data-role", "custom-select")

        super().__init__(attrs=attrs, *args, **kwargs)


class ProductForm(forms.Form):
    name = forms.CharField(validators=[validate_uppercase])
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField(min_value=0)
    category = forms.ChoiceField(
        choices=[
            ("phones", "Phones"),
            ("laptops", "Laptops"),
            ("tablets", "Tablets"),
        ],
        widget=FancySelect()
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")

        if len(phone) < 9:
            raise forms.ValidationError("Phone number is too short")

        return phone
