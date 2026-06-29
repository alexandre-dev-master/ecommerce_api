from django.db import models

class Products(models.Model):
    """
    Represents a Product entity within the e-Commerce system.
    Stores essential information such as name, description, price, and stock levels.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
   
    def __str__(self):
        """
        Returns a readable string representation of the product instance,
        useful for the admin interface and logging.
        """
        return f"{self.name}"