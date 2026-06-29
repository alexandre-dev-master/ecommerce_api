from rest_framework import viewsets
from .models import Products
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing product instances.
    Provides automatic CRUD actions mapped to standard HTTP methods.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer