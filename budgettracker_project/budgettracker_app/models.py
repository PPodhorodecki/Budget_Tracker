from datetime import date
from django.db import models


class User(models.Model):
    login = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    email = models.EmailField(max_length=64)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    account_created = models.DateField(default=date.today)
    last_log = models.DateTimeField(null=True)


class Session(models.Model):
    session_name = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Expense(models.Model):
    name = models.CharField(max_length=32)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    pay_month = models.DateField()
    pay_year = models.DateField()
    deadline = models.DateField(null=True)
    continuity = models.BooleanField(default=False)
    continuity_months = models.IntegerField(default=1)
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
    expanse = models.ForeignKey(Expense, on_delete=models.CASCADE)