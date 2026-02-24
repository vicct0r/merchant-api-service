from django.shortcuts import render
from rest_framework import generics

from .models import Client
from .serializers import ClientSerializer
from CustomMixins import TenantMixin


class ClientListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = ClientSerializer


class ClientListAPIView(TenantMixin, generics.ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)


class ClientRetrieveUpdateDestroy(TenantMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)