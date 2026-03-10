from rest_framework import serializers
from auditlog.models import LogEntry


class AuditLogSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    action = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = ['id', 'object_id', 'object_repr', 'action', 'changes', 'timestamp', 'actor']

    def get_action(self, obj) -> str:
        return obj.get_action_display()