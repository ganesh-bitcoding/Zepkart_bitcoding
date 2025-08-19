from django.db import models
from django.contrib.auth.models import User
from UserAccounts.models import Seller
from django.contrib.postgres.fields import ArrayField 

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)

    # Images
    images = ArrayField(models.ImageField(upload_to='product_images/'), blank=True, default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.seller.username})"
