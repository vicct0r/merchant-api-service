from django.db import models
from django.conf import settings


class AuditBaseModel(models.Model):
    class Operations(models.TextChoices):
        UPDATED = "updated", "Updated",
        CREATED = "created", "Created",
        DELETED = "deleted", "Deleted",

    created = models.DateTimeField(auto_now_add=True)
    edited_by = models.EmailField()
    workplace = models.ForeignKey('merchants.Workplace', on_delete=models.SET_NULL)
    operation = models.CharField(max_length=10, choices=Operations.choices)


class ClientsAuditModel(AuditBaseModel):
    client_id = models.UUIDField()
    client_name = models.CharField(max_length=200)
    client_phone = models.CharField(max_length=20)
    client_observations = models.TextField()


class ProductsAuditModel(AuditBaseModel):
    product_id = models.UUIDField()
    product_name = models.CharField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.PositiveIntegerField()
    product_sku = models.CharField(max_length=10)


class WorkplaceAuditModel(AuditBaseModel):
    workplace_id = models.UUIDField()
    workplace_name = models.CharField(max_length=150)
    workplace_cnpj = models.CharField(max_length=50)
    workplace_whitelist = models.JSONField(default=list)
