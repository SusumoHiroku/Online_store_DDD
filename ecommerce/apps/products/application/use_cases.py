from apps.products.domain.models import Product
from apps.products.infrastructure.repositories import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def list_products(self, filters=None):
        """Получает список товаров с фильтрацией."""
        return self.repository.get_all(filters)

    def add_product(self, product_data):
        """Добавляет новый товар."""
        product = Product(**product_data)
        return self.repository.save(product)

    def update_price(self, product_id, new_price):
        """Обновляет цену товара."""
        product = self.repository.get_by_id(product_id)
        if product:
            product.price = new_price
            self.repository.save(product)
        return product

    def start_promotion(self, product_id, discount):
        """Запускает акцию для товара."""
        product = self.repository.get_by_id(product_id)
        if product:
            product.apply_discount(discount)
            self.repository.save(product)
        return product

    def delete_product(self, product_id):
        """Удаляет товар."""
        return self.repository.delete(product_id)