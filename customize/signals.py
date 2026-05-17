from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    """Signal handler for creating products"""
    if created:
        print(f"New product created: {instance.name} - {instance.price}")