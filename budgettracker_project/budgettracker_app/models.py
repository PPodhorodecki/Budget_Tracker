from django.db import models


class User(models.Model):
    login = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    email = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    account_created = models.DateField()
    last_log = models.DateTimeField(null=True, default=0)