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
