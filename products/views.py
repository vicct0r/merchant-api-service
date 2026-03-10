from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from . import models
from .serializers import ProductCatalogSerializer, ProductSerializer
from merchants.mixins import TenantMixin
from config.serializers import AuditLogSerializer
from auditlog.models import LogEntry


class ProductListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = models.Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(workplace=self.request.user.workplace)


class ProductLogsListAPIView(generics.ListAPIView):
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        qs = models.Product.objects.filter(workplace=self.request.user.workplace)
        return LogEntry.objects.get_for_objects(qs)