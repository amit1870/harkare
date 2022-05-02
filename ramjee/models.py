from django.db import models
from accounts.models import Manushya

VIBHAKTI = [
    ('KH', 'Kahani'),
    ('SH', 'Shashtra'),
    ('VD', 'Ved'),
    ('PN', 'Puran'),
    ('LK', 'Lokmanya'),
    ('KY', 'Kavya'),
    ('PY', 'Padya'),
    ('PM', 'Prem'),
    ('BR', 'Gyan'),
    ('SR', 'Siyaram'),
]

class Harkare(models.Model):
    manushya = models.ForeignKey(Manushya, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    url = models.TextField(blank=True)
    vibhakti = models.CharField(max_length=2, choices=VIBHAKTI, default='SR')

    def __str__(self):
        return self.name
