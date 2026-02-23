from rest_framework import serializers
from .models import CustomUser
from rest_framework import serializers


class CustomUserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']