import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_label = self.user.username if self.user else f"Session {self.session_key[:8] if self.session_key else 'guest'}"
        return f"Cart ({user_label})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def line_total(self):
        return self.product.price * self.quantity

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery (Nepal)'),
        ('ESEWA', 'eSewa Sandbox (Online Test Payment)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Verified Paid'),
        ('FAILED', 'Failed / Cancelled'),
    ]

    ORDER_STATUS_CHOICES = [
        ('PLACED', 'Order Placed'),
        ('PROCESSING', 'Processing & Packing in Kathmandu Hub'),
        ('SHIPPED', 'Dispatched / In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Customer Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, help_text="e.g. 98XXXXXXXX")
    delivery_address = models.CharField(max_length=255, help_text="Street address / Tole / Landmark")
    city = models.CharField(max_length=100, default='Kathmandu')
    district = models.CharField(max_length=100, default='Kathmandu')
    order_notes = models.TextField(blank=True, help_text="Special delivery notes or gate directions")

    # Payment & Totals (in NPR)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PLACED')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('100.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.order_number = f"CURL-NP-{random_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name} (NPR {self.total_amount})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def line_total(self):
        return self.price * self.quantity

class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    transaction_uuid = models.CharField(max_length=100, unique=True)
    transaction_code = models.CharField(max_length=100, blank=True, help_text="eSewa Reference ID")
    provider = models.CharField(max_length=50, default='eSewa Sandbox')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, default='PENDING')
    raw_response = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - UUID: {self.transaction_uuid} ({self.status})"
