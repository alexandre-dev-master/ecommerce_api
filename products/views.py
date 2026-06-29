from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Products
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing product instances.
    Includes built-in support for filtering, full-text search, and ordering.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    
    # Configure filtering backends specifically for this view
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Exact match filters
    filterset_fields = ['stock']
    
    # Text search fields (maps to HTTP query param '?search=')
    search_fields = ['name', 'description']
    
    # Order parameters (maps to HTTP query param '?ordering=')
    ordering_fields = ['price', 'stock']