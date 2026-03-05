from rest_framework import serializers
from django.utils import timezone

from .models import Order, OrderItem
from clients.models import Client
from clients.serializers import ClientBasicSerializer
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    client_data = ClientBasicSerializer(source='client', read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id', 'client', 'status', 'due_date', 'total_price', 'client_data']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
        write_only=True
    )
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)
    unit_price = serializers.DecimalField(source='product.price', read_only=True, decimal_places=2, max_digits=10)

    class Meta:
        model = OrderItem
        fields = ['product', 'order', 'sku', 'quantity', 'unit_price']
        

class OrderRetrieveSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True
    )
    ordered_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'client', 'status', 'due_date', 'ordered_items']
        read_only_fields = ['id']

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Date/Time not valid for due date.')
        return value


