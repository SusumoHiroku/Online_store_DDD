from typing import Optional, List
from apps.orders.domain.models import Order, OrderStatus
from apps.orders.infrastructure.models import Order as OrderORM

class OrderRepository:

    def get_all(self) -> List[Order]:
        orm_orders = OrderORM.objects.all()
        return [self._map_to_domain(orm_order) for orm_order in orm_orders]

    def get_by_id(self, order_id: int) -> Optional[Order]:
        orm_order = OrderORM.objects.filter(id=order_id).first()
        return self._map_to_domain(orm_order) if orm_order else None

    def save(self, order: Order) -> Order:
        orm_order, created = OrderORM.objects.update_or_create(
            id=order.id,
            defaults={
                'product_id': order.product_id,
                'quantity': order.quantity,
                'status': order.status.value,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
            }
        )
        return self._map_to_domain(orm_order)

    def _map_to_domain(self, orm_order: OrderORM) -> Order:
        return Order(
            id=orm_order.id,
            product_id=orm_order.product_id,
            quantity=orm_order.quantity,
            status=OrderStatus(orm_order.status),
            created_at=orm_order.created_at,
            updated_at=orm_order.updated_at,
        )
