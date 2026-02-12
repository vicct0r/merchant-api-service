from django.shortcuts import render
from rest_framework import generics

from .models import Client
from .serializers import ClientSerializer


class OwnerFilterMixin:

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientListCreateAPIView(OwnerFilterMixin, generics.ListCreateAPIView):
    serializer_class = ClientSerializer


class ClientListAPIView(OwnerFilterMixin, generics.ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)


class ClientRetrieveUpdateDestroy(OwnerFilterMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)