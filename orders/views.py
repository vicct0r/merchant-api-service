from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.utils import timezone
from rest_framework import permissions, response
from rest_framework.views import APIView
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from CustomMixins import TenantMixin
from products.models import Product
    

class OrderListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(workplace=self.request.user.workplace)

    def get_queryset(self):
        qs = super().get_queryset()

        status = self.request.query_params.get("status")
        if status in ['dl', 'pd', 'or', 'is', 'ip']:
            qs = qs.filter(status=status)
        
        return qs.exclude(due_date__lt=timezone.now())


class AllOrdersListAPIView(TenantMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderRetrieveUpdateDestroy(TenantMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemCreateAPIView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _product = serializer.validated_data['product']
        p = get_object_or_404(Product, id=_product.id, workplace=request.user.workplace)
        serializer.save(order=order, unit_price=p.price)
        return response.Response(serializer.data)


class OrderItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def perform_update(self, serializer):
        return super().perform_update(serializer)
