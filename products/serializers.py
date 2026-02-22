from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ['id', 'workplace', 'created', 'modified']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Product price cannot be lower than 0.')
        return value
    
    def validate_sku(self, value):
        return value.upper()


class ProductCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['sku', 'name', 'price', 'quantity']
        read_only_fields = ['sku', 'name', 'price', 'quantity']
