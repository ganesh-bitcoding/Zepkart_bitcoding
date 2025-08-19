from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    BUSINESS_CHOICES = [
        ("individual", "Individual"),
        ("sole", "Sole Proprietorship"),
        ("partnership", "Partnership"),
        ("company", "Company"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    store_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    business_type = models.CharField(max_length=20, choices=BUSINESS_CHOICES, default="individual")
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)

    bank_account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)

    pickup_address = models.TextField(blank=True, null=True)
    return_address = models.TextField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_name} ({self.user.username})"