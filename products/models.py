from django.db import models
from django.core.exceptions import ValidationError
import uuid


class BaseProductDomain(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    workplace = models.ForeignKey('merchants.Workplace', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract=True


class Product(BaseProductDomain):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=12)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def clean(self):
        if self.price <= 0:
            raise ValidationError('Price cannot be lower or equal 0.')

    class Meta:
        unique_together=[('workplace', 'sku')]
