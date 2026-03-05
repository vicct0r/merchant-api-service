from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.utils import timezone
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, Sum

from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from merchants.mixins import TenantMixin
from products.models import Product
    

class OrderListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            total_price=Sum(
                F('ordered_items__unit_price') * F('ordered_items__quantity')
            )
        )

        status = self.request.query_params.get("status")
        if status in ['pending', 'delivered', 'on_route', 'in_preparation', 'returned', 'scheduled']:
            qs = qs.filter(status=status)
        
        return qs.exclude(due_date__lt=timezone.now())

    def perform_create(self, serializer):
        workplace = self.request.user.workplace
        serializer.save(workplace=workplace)


class AllOrdersListAPIView(TenantMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderRetrieveUpdateDestroy(TenantMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'


class OrderItemCreateAPIView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        product = data['product']        
        
        serializer.save(order=order, unit_price=product.price)

        if product.quantity < data['quantity'] and order.status != Order.Status.SCHEDULED:
            message = f"Your current batch is not enought for this sale."
        else:
            message = f"Product added to order {order.id}"

        return Response({
            "message": message,
            "data": serializer.data,
        })


class OrderItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def perform_update(self, serializer):
        return super().perform_update(serializer)
