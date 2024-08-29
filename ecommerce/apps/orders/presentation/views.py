from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.orders.application.use_cases import OrderService
from apps.orders.presentation.serializers import OrderSerializer, OrderReserveSerializer
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(viewsets.ViewSet):
    service = OrderService()

    def list(self, request):
        orders = self.service.order_repo.get_all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = self.service.order_repo.get_by_id(pk)
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=OrderReserveSerializer,
        responses={201: OrderSerializer}
    )
    @action(detail=False, methods=['post'])
    def reserve(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        try:
            order = self.service.reserve_product(product_id, quantity)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            order = self.service.cancel_reservation(pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        try:
            order = self.service.complete_sale(pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
