import datetime
from django.core.management.base import BaseCommand
from support.models import Order, ReturnRequest, StockItem


class Command(BaseCommand):
    help = 'Seeds demo orders, return requests, and stock items for Northstar Support MVP'

    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')

        # Seed Stock Items
        stock_items = [
            {'product_name': 'Northstar Classic Sneakers', 'sku': 'SNK-001', 'variant': 'Size 42 - White', 'in_stock': True, 'quantity': 28},
            {'product_name': 'Northstar Heavyweight Hoodie', 'sku': 'HD-002', 'variant': 'Size L - Black', 'in_stock': True, 'quantity': 15},
            {'product_name': 'Northstar Minimalist Cap', 'sku': 'CP-003', 'variant': 'One Size - Navy', 'in_stock': True, 'quantity': 42},
            {'product_name': 'Northstar Denim Jacket', 'sku': 'JK-004', 'variant': 'Size M - Blue', 'in_stock': False, 'quantity': 0},
        ]

        for item in stock_items:
            StockItem.objects.update_or_create(sku=item['sku'], defaults=item)

      # Seed Orders
        orders_data = [
            {'order_number': 'NS-1001', 'customer_name': 'Alice Johnson', 'customer_email': 'alice@example.com', 'status': 'shipped', 'tracking_number': 'TRK-9901', 'carrier': 'DHL Express', 'estimated_delivery': datetime.date(2026, 8, 18)},
            {'order_number': 'NS-1002', 'customer_name': 'Bob Smith', 'customer_email': 'bob@example.com', 'status': 'processing', 'tracking_number': 'TRK-9902', 'carrier': 'FedEx', 'estimated_delivery': datetime.date(2026, 8, 20)},
            {'order_number': 'NS-1003', 'customer_name': 'Charlie Brown', 'customer_email': 'charlie@example.com', 'status': 'delivered', 'tracking_number': 'TRK-9903', 'carrier': 'UPS', 'estimated_delivery': datetime.date(2026, 8, 14)},
            {'order_number': 'NS-1004', 'customer_name': 'David Miller', 'customer_email': 'david@example.com', 'status': 'shipped', 'tracking_number': 'TRK-9904', 'carrier': 'DHL Express', 'estimated_delivery': datetime.date(2026, 8, 19)},
            {'order_number': 'NS-1005', 'customer_name': 'Eve Adams', 'customer_email': 'eve@example.com', 'status': 'delivered', 'tracking_number': 'TRK-9905', 'carrier': 'FedEx', 'estimated_delivery': datetime.date(2026, 8, 12)},
        ]

        for odata in orders_data:
            order, _ = Order.objects.update_or_create(order_number=odata['order_number'], defaults=odata)
            if odata['order_number'] == 'NS-1001':
                ReturnRequest.objects.get_or_create(order=order, defaults={'reason': 'Size too small', 'status': 'approved', 'refund_eta': datetime.date(2026, 8, 22)})

        self.stdout.write(self.style.SUCCESS('Successfully seeded demo data for Group 83 MVP!'))