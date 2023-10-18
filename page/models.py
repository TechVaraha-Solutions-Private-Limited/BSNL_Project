from django.db import models

# Create your models here.
# class Sample(models.Model):


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=40)
    messages = models.CharField(max_length=100)