from typing import Optional
from apps.products.domain.models import Product
from apps.products.infrastructure.models import Product as ProductORM

class ProductRepository:
    def get_all(self, filters=None):
        query = ProductORM.objects.all()
        if filters:
            if 'category' in filters:
                query = query.filter(category=filters['category'])
            if 'subcategory' in filters:
                query = query.filter(subcategory=filters['subcategory'])
        return [self._map_to_domain(p) for p in query]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        orm_product = ProductORM.objects.filter(id=product_id).first()
        return self._map_to_domain(orm_product) if orm_product else None

    def save(self, product: Product) -> Product:
        orm_product, created = ProductORM.objects.update_or_create(
            id=product.id,
            defaults={
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'category': product.category,
                'subcategory': product.subcategory,
                'discount': product.discount,
            }
        )
        return self._map_to_domain(orm_product)

    def delete(self, product_id: int):
        ProductORM.objects.filter(id=product_id).delete()

    def _map_to_domain(self, orm_product: ProductORM) -> Product:
        return Product(
            id=orm_product.id,
            name=orm_product.name,
            description=orm_product.description,
            price=orm_product.price,
            stock=orm_product.stock,
            category=orm_product.category,
            subcategory=orm_product.subcategory,
            discount=orm_product.discount,
        )