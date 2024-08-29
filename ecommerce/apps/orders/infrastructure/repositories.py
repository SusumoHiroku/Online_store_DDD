from typing import Optional, List
from apps.orders.domain.models import Order, OrderStatus
from apps.orders.infrastructure.models import Order as OrderORM

class OrderRepository:
    """Репозиторий для работы с заказами."""

    def get_all(self) -> List[Order]:
        """
        Возвращает все заказы из базы данных.

        :return: Список заказов.
        """
        orm_orders = OrderORM.objects.all()
        return [self._map_to_domain(orm_order) for orm_order in orm_orders]

    def get_by_id(self, order_id: int) -> Optional[Order]:
        """
        Возвращает заказ по ID.

        :param order_id: Идентификатор заказа.
        :return: Заказ или None, если не найден.
        """
        orm_order = OrderORM.objects.filter(id=order_id).first()
        return self._map_to_domain(orm_order) if orm_order else None

    def save(self, order: Order) -> Order:
        """
        Сохраняет заказ в базе данных.

        :param order: Доменная модель заказа.
        :return: Сохраненный заказ.
        """
        try:
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
        except Exception as e:
            raise ValueError(f"Failed to save order: {e}")

    def _map_to_domain(self, orm_order: OrderORM) -> Order:
        """
        Преобразует ORM модель в доменную модель.

        :param orm_order: ORM модель заказа.
        :return: Доменная модель заказа.
        """
        return Order(
            id=orm_order.id,
            product_id=orm_order.product_id,
            quantity=orm_order.quantity,
            status=OrderStatus(orm_order.status),
            created_at=orm_order.created_at,
            updated_at=orm_order.updated_at,
        )
