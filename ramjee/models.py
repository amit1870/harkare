from django.db import models
from accounts.models import Manushya


class Harkare(models.Model):
    manushya = models.ForeignKey(Manushya, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    url = models.TextField(blank=True)

    def __str__(self):
        return self.name
