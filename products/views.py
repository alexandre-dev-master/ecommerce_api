from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Products, Category
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, CategorySerializer, RegisterSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing product categories.
    Only administrators can write/modify categories; anyone can view.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing product instances.
    Includes built-in support for filtering, full-text search, and ordering.
    Only administrators can write/modify products; anyone can view.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stock', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'stock']
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]     


class RegisterView(APIView):
    """
    Endpoint to register a new regular customer.
    Accessible by anyone (anonymous users).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)