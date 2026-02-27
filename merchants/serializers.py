from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from . import models

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
        read_only_fields = ['email']


class WorkplaceSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(source='whitelist', many=True, read_only=True)

    class Meta:
        model = models.Workplace
        fields = ['id', 'created_at', 'modified', 'owner', 'members']
        read_only_fields = ['id', 'created_at', 'modified', 'owner', 'members']


class WorkplaceMemberSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(source='whitelist', many=True, read_only=True)

    class Meta:
        model = models.Workplace
        fields = ['created_at', 'name', 'cnpj', 'members']
        read_only_fields = ['created_at', 'name', 'cnpj', 'members']
        
        
class WorkplaceMinimalSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = models.Workplace
        fields = ['name', 'cnpj', 'owner']
        read_only_fields = ['name', 'cnpj', 'owner']
    
    def get_owner(self, obj):
        return obj.owner.email


class AcceptInviteToWorkplaceSerializer(serializers.ModelSerializer):
    workplace_id = serializers.UUIDField()

    class Meta:
        model = models.Workplace
        fields = ['workplace_id']


class WhitelistAddUserSerializer(serializers.Serializer):
    user = serializers.EmailField()

    def validate_email(self, value):
        workplace = self.instance
        guest = User.objects.filter(email=value)
        if guest in workplace.whitelist.all():
            raise serializers.ValidationError('This user is already from this workplace.')
        return value