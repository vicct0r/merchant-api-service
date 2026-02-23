from django.db import models
from django.core.exceptions import ValidationError
import uuid

from django.conf import settings


class BaseMerchantDomain(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Workplace(BaseMerchantDomain):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ownership', on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    def clean_owner(self):
        if self.objects.filter(owner=self.owner).exists():
            raise ValidationError('You cannot own more than one workplace.')

