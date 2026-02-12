from rest_framework import serializers
from django.utils import timezone

from .models import Order
from clients.models import Client


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=Order.Status.choices
    )
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created', 'owner']

    def validate_client(self, value):
        if not Client.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError('Client not found on database.')
        return value

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Date/Time not valid for due date.')
        return value

    