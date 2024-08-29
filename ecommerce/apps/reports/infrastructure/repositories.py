from typing import List, Dict
from apps.orders.infrastructure.models import Order as OrderORM
from apps.orders.domain.models import OrderStatus

class ReportRepository:

    def get_sold_products_report(self, filters: Dict = None) -> List[Dict]:
        filters = filters or {}

        query = OrderORM.objects.filter(status=OrderStatus.SOLD.value)

        if 'category' in filters and filters['category']:
            query = query.filter(product__category=filters['category'])
        if 'subcategory' in filters and filters['subcategory']:
            query = query.filter(product__subcategory=filters['subcategory'])

        query = query.select_related('product')

        report = []
        for order in query:
            report.append({
                'order_id': order.id,
                'product_id': order.product.id,
                'product_name': order.product.name,
                'quantity_sold': order.quantity,
                'category': order.product.category,
                'subcategory': order.product.subcategory,
                'sale_date': order.updated_at,
            })
        return report
