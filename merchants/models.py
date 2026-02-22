from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid


class BaseMerchantDomain(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

# isso nao vai servir, precisamos categorizar corretamente, ou seja
# owner = merchantstaffmember
# refatorar isso antes de mais nada (logica central para buscar objetos de workplaces isoladamente).
class Workplace(BaseMerchantDomain):
    owner = models.OneToOneField(User, related_name='workplace', on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True)
    cnpj = models.CharField(max_length=25, unique=True)
    users = models.ManyToManyField(User, related_name='valid_workplaces')

    def __str__(self):
        return self.cnpj
    
    def clean_owner(self):
        if self.objects.filter(owner=self.owner).exists():
            raise ValidationError('You cannot own more than one workplace.')


class MerchantStaffProfile(BaseMerchantDomain):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, related_name='members', on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    def clean_user(self):
        if self.workplace.owner == self.user:
            raise ValidationError('The workplace owner cannot be staff member.')

        if self.user not in self.workplace.users.all():
            raise ValidationError('You cannot join this workplace due to restrictions reasons.')

