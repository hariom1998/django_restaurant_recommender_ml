from django.db import models
from django.contrib.auth.models import AbstractUser
from restrecommender.models import Restaurantdata


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False)
    locality = models.CharField(max_length=100, blank=False)


class history(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    restname = models.ForeignKey(
        Restaurantdata, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
