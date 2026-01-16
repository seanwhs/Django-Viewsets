# products/models.py
from django.db import models

class Product(models.Model):  
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
