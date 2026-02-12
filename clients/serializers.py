from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id']

    def validate_name(self, value):
        if any(i.isdigit() for i in value):
            raise serializers.ValidationError('Names can not contain numbers.')
        return value