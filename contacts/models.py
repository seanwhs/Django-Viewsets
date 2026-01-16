# contacts/models.py
from django.db import models

class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)

    def __str__(self):
        return self.lname  
