from django.conf import settings
from django.dispatch import receiver
from django.db.models import signals
from . import models


@receiver(signals.post_save, sender='clients.Client', receiver='audit.ClientAuditModel')
def create_client_audit_object(sender, instance, created, **kwargs):
    """Create an audition object when client is created/updated/deleted."""
    _operation = str() 
    if created:
        _operation = models.AuditBaseModel.Operations.CREATED
        

