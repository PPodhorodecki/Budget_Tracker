# Generated by Django 4.0 on 2022-01-18 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgettracker_app', '0013_alter_expense_exp_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='continuity_step',
        ),
    ]