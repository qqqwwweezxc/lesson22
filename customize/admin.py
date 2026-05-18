from django.contrib import admin
from django.db.models import F
from .models import Product, Review
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Register users with custom admin site"""
    list_display = [
        "username",
        "email",
        "phone_number",
        "is_staff",
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("phone_number",)
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": ("phone_number",)
            },
        ),
    )


class ReviewInline(admin.TabularInline):
    """Inline for reviews"""
    model = Review
    extra = 1


class HasInStockFilter(admin.SimpleListFilter):
    """Filter by in-stock products"""
    title = 'In stock'
    parameter_name = 'in_stock'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'In stock'),
            ('no', 'Out of stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(quantity__gt=0)
        if self.value() == 'no':
            return queryset.filter(quantity=0)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Register model Product with admin site"""
    list_display = ["name", "price", "quantity"]
    search_fields = ["name"]
    list_filter = ["price", HasInStockFilter]
    actions = ["add_to_stock", "remove_from_stock"]
    inlines = [ReviewInline]

    def add_to_stock(self, request, queryset):
        queryset.update(quantity=F("quantity") + 1)

    add_to_stock.short_description = "Add 1 product to stock"

    def remove_from_stock(self, request, queryset):
        queryset.filter(quantity__gt=0).update(
            quantity=F("quantity") - 1
        )

    remove_from_stock.short_description = "Remove 1 product from stock"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Register model Review with admin site"""
    list_display = ["product", "rating"]