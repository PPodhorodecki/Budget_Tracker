# Generated by Django 4.0 on 2022-01-08 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgettracker_app', '0005_remove_expense_continuity_months_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Session',
        ),
    ]
