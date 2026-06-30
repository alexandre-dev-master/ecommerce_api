from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Products

class ProductAPITests(APITestCase):

    def setUp(self):
        # Create a standard user for authentication tests
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create an initial product for testing GET/PUT/DELETE
        self.product = Products.objects.create(
            name="Test_Keyboard",
            description="mechanical keyboard",
            price="150.00",
            stock=10
        )
        
        # URL dynamic resolution
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

    def test_anonymous_user_can_list_products(self):
        """Validates that any non-logged visitor can view the products list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_create_product(self):
        """Validates that anonymous users are blocked from creating products (HTTP 403)."""
        data = {"name": "Mouse Teste", "price": "50.00", "stock": 5, "description": "Sem fio"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_product(self):
        """Validates that a logged-in user can successfully create a product."""
        self.client.login(username='testuser', password='password123')
        data = {"name": "Mouse Teste", "price": "50.00", "stock": 5, "description": "Sem fio"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_serializer_validation_invalid_price(self):
        """Validates that the price validator blocks values equal to or less than zero."""
        self.client.login(username='testuser', password='password123')
        data = {"name": "Item Invalido", "price": "0.00", "stock": 5, "description": "Erro esperado"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)