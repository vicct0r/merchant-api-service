from django.db import models
import uuid
from django.core.exceptions import ValidationError

from auditlog.registry import auditlog


class BaseOwnershipModel(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    workplace = models.ForeignKey('merchants.Workplace', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract=True


class Order(BaseOwnershipModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ON_ROUTE = "on_route", "On route"
        DELIVERED = "delivered", "Delivered"
        ISSUE = "issue", "Issue"
        IN_PREPARATION = "in_preparation", "In preparation"
        RETURNED = "returned", "Returned"
        SCHEDULED = "scheduled", "Scheduled"
    
    client = models.ForeignKey('clients.Client', related_name='client_orders', on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)
    products = models.ManyToManyField('products.Product', related_name='orders', through='OrderItem')

    def __str__(self):
        return f"Order {self.id} - due {self.due_date}"
    
    def clean(self):
        if not self.pk:
            return
        
        invalid_status = [self.Status.DELIVERED, self.Status.RETURNED]
        
        previous = Order.objects.get(pk=self.pk)
        if previous.status in invalid_status:
            raise ValidationError('Delivered and returned orders cannot be modified.')
        

class OrderItem(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey('orders.Order', related_name='ordered_items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='ordered_item', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'x{self.quantity} - {self.product.name}'
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Cannot order 0 or less unities of products.')


class Reversal(BaseOwnershipModel):
    order = models.ForeignKey(Order, related_name='reversal', on_delete=models.CASCADE)
    observations = models.TextField()

    def __str__(self):
        return self.order.id

    def clean(self):
        if not Order.objects.filter(workplace=self.workplace).exists():
            raise ValidationError('Order not found.')
        
        if not self.order.workplace == self.workplace:
            raise ValidationError('You dont have ownership to this order.')


auditlog.register(Order)
