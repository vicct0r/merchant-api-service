from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework import permissions
from .serializers import OrderSerializer
from .models import Order


class OwnerFilterMixin:
    def get_queryset(self):
        return Order.objects.filter(owner=self.request.user)
    

class OrderListCreateAPIView(OwnerFilterMixin, generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        status = self.request.query_params.get("status")
        if status in ['dl', 'pd', 'or', 'is', 'ip']:
            qs = qs.filter(status=status)
        
        return qs.exclude(due_date__lt=timezone.now())


class AllOrdersListAPIView(OwnerFilterMixin, generics.ListAPIView):
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroy(OwnerFilterMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

