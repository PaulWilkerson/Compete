from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    website = models.CharField(max_length=90)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    about = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
