# Generated by Django 4.0 on 2022-01-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgettracker_app', '0012_expense_next_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='exp_create',
            field=models.DateField(),
        ),
    ]
