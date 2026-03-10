from django.db import models
import uuid
from auditlog.registry import auditlog


class Client(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    workplace = models.ForeignKey('merchants.Workplace', related_name='clients', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    observations = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

auditlog.register(Client)
