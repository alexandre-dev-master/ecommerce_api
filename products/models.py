from django.db import models

class Category(models.Model):
    """
    Represents a product category within the e-Commerce system.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the category.
        """
        return f"{self.name}"

class Products(models.Model):
    """
    Represents a Product entity within the e-Commerce system.
    Stores essential information such as name, description, price, and stock levels.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    # Relationship: One Category can have multiple Products
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        null=True, 
        blank=True
    )
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        """
        Returns a readable string representation of the product instance.
        """
        return f"{self.name}"