from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    """Custom serializer for reviews"""
    class Meta:
        model = Review
        fields = ["id", "text", "rating"]


class ProductSerializer(serializers.ModelSerializer):
    """Custom serializer for products"""
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'reviews']