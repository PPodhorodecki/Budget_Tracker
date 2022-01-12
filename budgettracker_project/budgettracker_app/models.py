from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Expense(models.Model):
    name = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    deadline = models.DateField(null=True)
    continuity = models.BooleanField(default=False)
    continuity_step = models.IntegerField(null=True) #Jak często płatność, jeśli damy, że cyklicznie. Dać defaultowo miesiąc.
    continuity_amount = models.IntegerField(null=True) #Ile cyklicznych płatności, jeśli damy, że cyklicznie.
    is_paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Note(models.Model):
    text = models.TextField()
    mod_date = models.DateField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)


class Archive(models.Model):
    name = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    paid_date = models.DateField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)