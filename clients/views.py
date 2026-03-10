from django.shortcuts import render
from rest_framework import generics, exceptions
from .models import Client
from .serializers import ClientSerializer
from merchants.mixins import TenantMixin
from auditlog.models import LogEntry
from config.serializers import AuditLogSerializer


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


class ClientLogListAPIView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    
    def get_queryset(self):
        qs = Client.objects.filter(workplace=self.request.user.workplace)
        return LogEntry.objects.get_for_objects(qs)