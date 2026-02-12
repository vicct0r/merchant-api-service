from django.db import models
from django.contrib.auth.models import User
import uuid


class Client(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, related_name='user_clients', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    observations = models.TextField()
    
    def __str__(self):
        return self.name
