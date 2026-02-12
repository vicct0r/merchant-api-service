from django.db import models
from django.contrib.auth.models import User
import uuid

from clients.models import Client


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ON_ROUTE = "on_route", "On route"
        DELIVERED = "delivered", "Delivered"
        ISSUE = "issue", "Issue"
        IN_PREPARATION = "in_preparation", "In preparation"


    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, related_name='user_orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    client = models.ForeignKey(Client, related_name='client_orders', on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.PENDING)

    def __str__(self):
        return self.due_date