from rest_framework import serializers
from django.utils import timezone

from .models import Order
from clients.models import Client
from clients.serializers import ClientBasicSerializer


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    client_data = ClientBasicSerializer(source='client', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created', 'status', 'due_date', 'client_data', 'workplace']
        read_only_fields = ['id', 'created', 'workplace', 'client_data']

    def validate_client(self, value):
        if not Client.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError('Client not found on database.')
        return value

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Date/Time not valid for due date.')
        return value

    