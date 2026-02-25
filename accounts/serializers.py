from rest_framework import serializers
from .models import CustomUser

class CustomUserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'is_staff', 'is_active', 'is_verified', 'email', 'workplace']