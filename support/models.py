from django.db import models


class Order(models.Model):
    """Represents a customer order. Staff create/edit; customers look up read-only."""

    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    tracking_number = models.CharField(max_length=50, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    shipping_address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_number} — {self.customer_name} ({self.get_status_display()})"

    def status_color(self):
        return {
            'processing': 'warning',
            'shipped': 'info',
            'delivered': 'success',
            'cancelled': 'danger',
        }.get(self.status, 'secondary')