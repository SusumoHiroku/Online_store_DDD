from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from apps.products.application.use_cases import ProductService
from apps.products.presentation.serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductViewSet(viewsets.ViewSet):
    service = ProductService()

    @swagger_auto_schema(
        operation_summary="Получить список товаров",
        operation_description="Возвращает список товаров с возможностью фильтрации по категории и подкатегории. "
                              "Только товары с остатком больше 0 будут включены в список.",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Фильтр по категории", type=openapi.TYPE_STRING),
            openapi.Parameter('subcategory', openapi.IN_QUERY, description="Фильтр по подкатегории", type=openapi.TYPE_STRING)
        ],
        responses={
            200: ProductSerializer(many=True),
            400: 'Неверные параметры запроса'
        }
    )
    def list(self, request):
        filters = request.query_params.dict()
        try:
            products = self.service.list_products(filters)
            paginator = PageNumberPagination()
            paginated_products = paginator.paginate_queryset(products, request)

            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ValidationError:
            return Response({"detail": "Неверные параметры запроса."}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Создать новый товар",
        operation_description="Добавляет новый товар.",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Ошибка валидации данных',
        }
    )
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = self.service.add_product(serializer.validated_data)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response({"detail": "Ошибка валидации данных."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Обновить цену товара",
        operation_description="Обновляет цену товара по заданному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Новая цена товара')
            },
            required=['price']
        ),
        responses={
            200: ProductSerializer,
            400: 'Ошибка валидации данных',
            404: 'Товар не найден'
        }
    )
    @action(detail=True, methods=['post'])
    def update_price(self, request, pk=None):
        new_price = request.data.get('price')
        if new_price is None:
            return Response({"detail": "Цена не указана."}, status=status.HTTP_400_BAD_REQUEST)

        product = self.service.update_price(pk, new_price)
        if product:
            return Response(ProductSerializer(product).data)
        return Response({"detail": "Товар не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Начать акцию на товар",
        operation_description="Применяет скидку к товару по заданному ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'discount': openapi.Schema(type=openapi.TYPE_NUMBER, format='float',
                                           description='Размер скидки в процентах')
            },
            required=['discount']
        ),
        responses={
            200: ProductSerializer,
            400: 'Ошибка валидации данных',
            404: 'Товар не найден'
        }
    )
    @action(detail=True, methods=['post'])
    def start_promotion(self, request, pk=None):
        discount = request.data.get('discount')
        if discount is None:
            return Response({"detail": "Скидка не указана."}, status=status.HTTP_400_BAD_REQUEST)

        product = self.service.start_promotion(pk, discount)
        if product:
            return Response(ProductSerializer(product).data)
        return Response({"detail": "Товар не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Удалить товар",
        operation_description="Удаляет товар по заданному ID.",
        responses={
            204: 'Товар успешно удален',
            404: 'Товар не найден'
        }
    )
    def destroy(self, request, pk=None):
        try:
            self.service.delete_product(pk)
            return Response({"detail": "Товар успешно удален."},status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"detail": "Товар не найден."}, status=status.HTTP_404_NOT_FOUND)
