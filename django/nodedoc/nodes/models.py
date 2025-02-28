from django.db import models

# Create your models here.
import uuid

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField(unique=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)
    online = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hostname or self.ip_address} ({'Online' if self.online else 'Offline'})"
