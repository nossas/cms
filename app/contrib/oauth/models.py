import uuid

from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User, related_name="auth_token", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = str(uuid.uuid4())
        
        super().save(*args, **kwargs)