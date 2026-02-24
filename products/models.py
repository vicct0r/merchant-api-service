from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from merchants.models import Workplace
import uuid


class BaseProductDomain(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract=True


class Product(BaseProductDomain):
    name = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=12, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def clean_price(self):
        if self.price < 0:
            raise ValidationError('Price cannot be lower than 0.')


class ProductsTransactions(BaseProductDomain):
    product = models.ForeignKey(Product, related_name='transactions', on_delete=models.CASCADE)
    operation = models.CharField(max_length=100)
    quantity = models.BigIntegerField()

    def __str__(self):
        return self.created

