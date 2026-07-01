from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Products, Category

class ProductAPITests(APITestCase):

    def setUp(self):
        # Create a standard user for non-admin authentication tests
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create an initial category for testing relationship and endpoints
        self.category = Category.objects.create(name="Electronics")
        
        # Create an initial product for testing GET/PUT/DELETE workflows
        self.product = Products.objects.create(
            name="Test_Keyboard",
            description="mechanical keyboard",
            price="150.00",
            stock=10,
            category=self.category
        )
        
        # Resolve URLs dynamically based on router registration names
        self.list_url = reverse('product-list')
        self.category_list_url = reverse('category-list')

    def test_anonymous_user_can_list_products(self):
        """Validates that any non-logged visitor can view the products list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_create_product(self):
        """Validates that anonymous users are completely blocked from creating products (HTTP 401)."""
        data = {"name": "Mouse Teste", "price": "50.00", "stock": 5, "description": "Sem fio"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_admin_can_create_product(self):
        """Validates that a logged-in ADMIN user (is_staff=True) can successfully create a product using JWT."""
        # Create an admin user explicitly setting the is_staff flag
        admin_user = User.objects.create_user(username='adminuser', password='password123', is_staff=True)
        
        # Generate the JWT cryptographic pair for the admin user
        refresh = RefreshToken.for_user(admin_user)
        
        # Inject the access token into the Authorization Bearer header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {"name": "Mouse Teste", "price": "50.00", "stock": 5, "description": "Sem fio", "category": self.category.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_authenticated_user_cannot_create_product(self):
        """Validates that a standard logged-in user (not admin) is strictly blocked from creating products (HTTP 403)."""
        # Generate token for the standard customer created in setUp (is_staff=False)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {"name": "Mouse Invasor", "price": "50.00", "stock": 5, "description": "Should fail"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_authenticated_user_cannot_create_category(self):
        """Validates that a standard logged-in user (not admin) is strictly blocked from creating categories (HTTP 403)."""
        # Generate token for the standard customer (is_staff=False)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {"name": "Hack Category"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_serializer_validation_invalid_price(self):
        """Validates that the price validator triggers bad request errors before writing to DB."""
        # Create an admin user so the request bypasses the initial authorization barrier
        admin_user = User.objects.create_user(username='validatoradmin', password='password123', is_staff=True)
        refresh = RefreshToken.for_user(admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {"name": "Item Invalido", "price": "0.00", "stock": 5, "description": "Erro esperado"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)