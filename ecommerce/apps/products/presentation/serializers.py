from rest_framework import serializers
from apps.products.domain.models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    category = serializers.CharField(max_length=255, required=False, allow_null=True)
    subcategory = serializers.CharField(max_length=255, required=False, allow_null=True)
    discount = serializers.FloatField(default=0.0)

    def create(self, validated_data):
        return Product(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.discount = validated_data.get('discount', instance.discount)
        return instance
