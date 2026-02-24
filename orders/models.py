from django.db import models
import uuid
from django.core.exceptions import ValidationError
from clients.models import Client
from merchants.models import Workplace


class BaseOwnershipModel(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
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
    
    client = models.ForeignKey(Client, related_name='client_orders', on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)

    def __str__(self):
        return f"Order {self.id} - due {self.due_date}"
    
    def clean_status(self):
        if not self.pk:
            return
        
        invalid_status = [self.Status.DELIVERED, self.Status.RETURNED]
        
        previous = Order.objects.get(pk=self.pk)
        if previous.status in invalid_status:
            raise ValidationError('Delivered and returned orders cannot be modified.')


class Reversal(BaseOwnershipModel):
    order = models.ForeignKey(Order, related_name='reversal', on_delete=models.CASCADE)
    observations = models.TextField()

    def __str__(self):
        return self.order

    def clean_order(self):
        if not Order.objects.filter(owner=self.owner).exists():
            raise ValidationError('Order not found.')
        
        if not self.order.workplace == self.workplace:
            raise ValidationError('You dont have ownership to this order.')
    

