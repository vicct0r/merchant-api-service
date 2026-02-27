from django.shortcuts import render
from rest_framework import generics, exceptions
from .models import Client
from .serializers import ClientSerializer
from CustomMixins import TenantMixin


class ClientListCreateAPIView(TenantMixin, generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.save(workplace=self.request.user.workplace)
        

class ClientListAPIView(TenantMixin, generics.ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)


class ClientRetrieveUpdateDestroy(TenantMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    lookup_field = 'id'
    queryset = Client.objects.all()