from django.db import models
from core.user.models import AppUser

# Create your models here.
class MailingGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(AppUser)

    def __str__(self):
        return self.name