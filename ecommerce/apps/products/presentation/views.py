from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.products.application.use_cases import ProductService
from apps.products.presentation.serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductViewSet(viewsets.ViewSet):
    service = ProductService()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category", type=openapi.TYPE_STRING),
            openapi.Parameter('subcategory', openapi.IN_QUERY, description="Filter by subcategory",
                              type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request):
        filters = request.query_params.dict()
        products = self.service.list_products(filters)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = self.service.add_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        new_price = request.data.get('price')
        product = self.service.update_price(pk, new_price)
        if product:
            return Response(ProductSerializer(product).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def start_promotion(self, request, pk=None):
        discount = request.data.get('discount')
        product = self.service.start_promotion(pk, discount)
        if product:
            return Response(ProductSerializer(product).data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        self.service.delete_product(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
