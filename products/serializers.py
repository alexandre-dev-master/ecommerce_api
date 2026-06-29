from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Products model instance into JSON format
    and handle data validation for creation and updates.
    """
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'stock']

    def validate_price(self, value):
        """
        Validates that the product price is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("The price must be greater than zero.")
        return value

    def validate_stock(self, value):
        """
        Validates that the stock quantity is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("The stock quantity cannot be negative.")
        return value