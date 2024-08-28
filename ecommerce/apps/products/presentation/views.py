from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.products.application.use_cases import ProductService

class ProductViewSet(viewsets.ViewSet):
    service = ProductService()

    def list(self, request):
        filters = request.query_params.dict()
        products = self.service.list_products(filters)
        return Response([self._serialize_product(p) for p in products])

    def create(self, request):
        product_data = request.data
        product = self.service.add_product(product_data)
        return Response(self._serialize_product(product), status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        new_price = request.data.get('price')
        product = self.service.update_price(pk, new_price)
        if product:
            return Response(self._serialize_product(product))
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def start_promotion(self, request, pk=None):
        discount = request.data.get('discount')
        product = self.service.start_promotion(pk, discount)
        if product:
            return Response(self._serialize_product(product))
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def destroy(self, request, pk=None):
        self.service.delete_product(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _serialize_product(self, product):
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'category': product.category,
            'subcategory': product.subcategory,
            'discount': product.discount,
        }