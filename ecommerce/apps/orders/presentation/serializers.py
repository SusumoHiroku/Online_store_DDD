from rest_framework import serializers
from apps.orders.domain.models import Order, OrderStatus

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    status = serializers.ChoiceField(choices=[(status.name, status.value) for status in OrderStatus])
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Order(**validated_data)

    def update(self, instance, validated_data):
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = OrderStatus(validated_data.get('status', instance.status.value))
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        return instance
