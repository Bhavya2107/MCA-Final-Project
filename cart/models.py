from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum


class Cart(models.Model):
    """Shopping cart per user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart of {self.user.username}"

    # ✅ Subtotal (without GST)
    def get_subtotal(self):
        """Total price without tax"""
        subtotal = self.items.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total']
        return subtotal or 0

    # ✅ GST (18%)
    def get_tax(self):
        """Calculate 18% GST"""
        return self.get_subtotal() * 0.18

    # ✅ Final Total (Subtotal + GST only)
    def get_total_price(self):
        """Final total (no shipping)"""
        return self.get_subtotal() + self.get_tax()

    # ✅ Total items count
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    # ✅ Clear cart
    def clear_cart(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual items in a user's cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    app_label = models.CharField(max_length=50)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'app_label', 'product_id')
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.product_name} x{self.quantity} (₹{self.price})"

    # ✅ Item subtotal
    def get_subtotal(self):
        """Subtotal for this item"""
        return self.price * self.quantity

    # ✅ Increase quantity
    def increase_quantity(self, amount=1):
        self.quantity += amount
        self.save()

    # ✅ Decrease quantity
    def decrease_quantity(self, amount=1):
        self.quantity -= amount
        if self.quantity <= 0:
            self.delete()
        else:
            self.save()


class Order(models.Model):
    """Store order information with delivery details"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
    ]
    
    # Order basic info
    order_id = models.CharField(max_length=20, unique=True)  # e.g., "LS-ABC123DEF456"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    
    # Delivery address
    delivery_full_name = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=20)
    delivery_email = models.EmailField()
    delivery_street_address = models.CharField(max_length=255)
    delivery_apartment = models.CharField(max_length=100, blank=True, null=True)
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=100)
    delivery_postal_code = models.CharField(max_length=20)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Before tax
    tax = models.DecimalField(max_digits=10, decimal_places=2)  # 18% GST
    delivery_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Free for Ahmedabad
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Subtotal + Tax + Delivery
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
    def get_full_address(self):
        """Return formatted full address"""
        address_parts = [
            self.delivery_street_address,
            self.delivery_apartment if self.delivery_apartment else '',
            self.delivery_city,
            self.delivery_state,
            self.delivery_postal_code,
        ]
        return ', '.join([p for p in address_parts if p])  # Remove empty strings


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    app_label = models.CharField(max_length=50)  # e.g., 'used_laptops', 'accessories'
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity} in {self.order.order_id}"
    
    def get_subtotal(self):
        """Get subtotal for this order item"""
        return self.product_price * self.quantity