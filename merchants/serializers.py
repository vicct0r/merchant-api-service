from rest_framework import serializers
from . import models


class WorkplaceCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workplace
        fields = '__all__'
        read_only_fields = ['id', 'created', 'modified', 'owner']

    def validate_owner(self, value):
        if models.Workplace.objects.filter(owner=value).exists():
            raise serializers.ValidationError('You cannot have more than one workplace.')


class InviteJoinWorkplaceSerializer(serializers.ModelSerializer):
    invite = serializers.UUIDField()

    class Meta:
        model = models.Workplace
        fields = ['id', 'created', 'user', 'workplace', 'role', 'invite']
        read_only_fields = ['id', 'created', 'user', 'workplace', 'role']

    def validate_invite(self, value):
        is_workplace = models.Workplace.objects.filter(id=value).exists()
        if not is_workplace:
            raise serializers.ValidationError('This workplace does not exist.')
        return value