from typing import Optional
from apps.orders.domain.models import Order, OrderStatus
from apps.orders.infrastructure.repositories import OrderRepository
from apps.products.infrastructure.repositories import ProductRepository
from django.db import transaction

class OrderService:
    def __init__(self):
        self.order_repo = OrderRepository()
        self.product_repo = ProductRepository()

    def reserve_product(self, product_id: int, quantity: int) -> Optional[Order]:
        """Резервирует товар, уменьшая его остаток и создавая заказ."""
        with transaction.atomic():
            product = self._get_product_or_raise(product_id)

            if product.stock < quantity:
                raise ValueError("Insufficient stock for reservation.")

            product.stock -= quantity
            self.product_repo.save(product)

            order = Order(id=None, product_id=product_id, quantity=quantity)
            return self.order_repo.save(order)

    def cancel_reservation(self, order_id: int) -> Optional[Order]:
        """Отменяет резервирование товара, возвращая количество."""
        order = self._get_order_or_raise(order_id)

        with transaction.atomic():
            order.cancel()
            product = self._get_product_or_raise(order.product_id)
            product.stock += order.quantity
            self.product_repo.save(product)
            return self.order_repo.save(order)

    def complete_sale(self, order_id: int) -> Optional[Order]:
        """Завершает продажу, меняя статус заказа на 'sold'."""
        order = self._get_order_or_raise(order_id)
        order.complete_sale()
        return self.order_repo.save(order)

    def _get_product_or_raise(self, product_id: int):
        """Возвращает продукт по ID или выбрасывает исключение."""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} does not exist.")
        return product

    def _get_order_or_raise(self, order_id: int) -> Order:
        """Возвращает заказ по ID или выбрасывает исключение."""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found.")
        return order
