from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workplace
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'owner', 'whitelist']

    def validate_whitelist(self, value):
        guest = User.objects.filter(email=value).exists()
        if not guest:
            raise serializers.ValidationError('User not found.')
        return value


class WorkplaceMinimalSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = models.Workplace
        fields = ['name', 'cnpj', 'owner']
        read_only_fields = ['name', 'cnpj', 'owner']
    
    def get_owner(self, obj):
        return obj.email

class InviteToWorkplaceSerializer(serializers.ModelSerializer):
    workplace_id = serializers.UUIDField()
    permission = serializers.SerializerMethodField()

    class Meta:
        model = models.Workplace
        fields = ['workplace_id', 'permission']
        read_only_fields = ['permission']    
    
    def get_permission(self, obj):
        whitelist = obj.whitelist.all()
        request = self.context.get('request')
        if request:
            user = request.user
        if not user in whitelist:
            obj = False
        obj = True
        return obj