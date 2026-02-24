from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from . import models
from .serializers import ProductCatalogSerializer, ProductSerializer
from CustomMixins import TenantMixin


class ProductListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    
    
