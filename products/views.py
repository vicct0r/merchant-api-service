from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from . import models
from .serializers import ProductCatalogSerializer, ProductSerializer
from merchants.mixins import TenantMixin


class ProductListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = models.Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(workplace=self.request.user.workplace)
    
    
