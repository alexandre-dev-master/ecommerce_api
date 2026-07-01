from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Products, Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to map the Category model into JSON format.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Products model and handle data validation.
    Includes nested category information for read operations.
    """
    category_detail = CategorySerializer(source='category', read_only=True)
    
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        write_only=True, 
        required=False
    )

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'category_detail']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("The stock levels cannot be negative.")
        return value
    
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer to handle user registration.
    Ensures the password is securely hashed before saving.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # The create_user method automatically hashes the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user