from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from apps.orders.application.use_cases import OrderService
from apps.orders.presentation.serializers import OrderSerializer, OrderReserveSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

class OrderViewSet(viewsets.ViewSet):
    service = OrderService()

    @swagger_auto_schema(
        operation_summary="Получить список заказов",
        operation_description="Возвращает список всех заказов с постраничной навигацией.",
        responses={
            200: OrderSerializer(many=True),
            400: 'Неверные параметры запроса'
        }
    )
    def list(self, request):
        orders = self.service.order_repo.get_all()
        paginator = PageNumberPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Получить заказ по ID",
        operation_description="Возвращает детали заказа по заданному ID.",
        responses={
            200: OrderSerializer,
            404: 'Заказ не найден'
        }
    )
    def retrieve(self, request, pk=None):
        try:
            order = self.service._get_order_or_raise(pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError:
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Зарезервировать товар",
        operation_description="Зарезервирует товар по ID и количеству.",
        request_body=OrderReserveSerializer,
        responses={
            201: OrderSerializer,
            400: 'Ошибка валидации данных',
            404: 'Товар не найден'
        }
    )
    @action(detail=False, methods=['post'])
    def reserve(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        try:
            order = self.service.reserve_product(product_id, quantity)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"detail": 'Ошибка валидации данных'}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response({"detail": "Товар не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Отменить резервирование заказа",
        operation_description="Отменяет резервирование заказа по заданному ID.",
        responses={
            200: OrderSerializer,
            400: 'Ошибка отмены резервации',
            404: 'Заказ не найден'
        }
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            order = self.service.cancel_reservation(pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError:
            return Response({"detail": 'Ошибка отмены резервации'}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Продажа товара",
        operation_description="Совершает продажу товара по заданному ID заказа.",
        responses={
            200: OrderSerializer,
            400: 'Ошибка завершения продажи',
            404: 'Заказ не найден'
        }
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        try:
            order = self.service.complete_sale(pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError:
            return Response({"detail": "Ошибка завершения продажи."}, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)

