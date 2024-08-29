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
        with transaction.atomic():
            product = self.product_repo.get_by_id(product_id)

            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")

            if product.stock < quantity:
                raise ValueError("Insufficient stock for reservation.")

            product.stock -= quantity
            self.product_repo.save(product)

            order = Order(id=None, product_id=product_id, quantity=quantity)
            return self.order_repo.save(order)

    def cancel_reservation(self, order_id: int) -> Optional[Order]:
        order = self.order_repo.get_by_id(order_id)
        if order:
            order.cancel()
            product = self.product_repo.get_by_id(order.product_id)
            product.stock += order.quantity
            self.product_repo.save(product)
            return self.order_repo.save(order)
        raise ValueError("Order not found or cannot be cancelled.")

    def complete_sale(self, order_id: int) -> Optional[Order]:
        order = self.order_repo.get_by_id(order_id)
        if order:
            order.complete_sale()
            return self.order_repo.save(order)
        raise ValueError("Order not found or cannot complete sale.")
