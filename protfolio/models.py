from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=256)
    message = models.TextField()
