from re import T
from django.db import models

# Create your models here.


class Whatsapp(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to='whatsappAvatar')
    draft = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name