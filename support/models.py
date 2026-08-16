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

    class ReturnRequest(models.Model):
   

     STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('refunded', 'Refunded'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    refund_eta = models.DateField(null=True, blank=True)
    staff_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Return #{self.pk} for {self.order.order_number} — {self.get_status_display()}"

    def status_color(self):
        return {
            'pending': 'warning',
            'approved': 'info',
            'rejected': 'danger',
            'refunded': 'success',
        }.get(self.status, 'secondary')

class StockItem(models.Model):
    """A product variant with current stock info. Staff maintain; customers query."""

    product_name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    variant = models.CharField(max_length=100, blank=True, help_text='e.g. Size L, Color Navy')
    in_stock = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)
    restock_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_name', 'variant']

    def __str__(self):
        stock_label = f"{self.quantity} in stock" if self.in_stock else "Out of stock"
        return f"{self.product_name} ({self.variant}) — {stock_label}"


class StockNotification(models.Model):
  

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='notifications')
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('stock_item', 'customer_email')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_email} → {self.stock_item.product_name}"
