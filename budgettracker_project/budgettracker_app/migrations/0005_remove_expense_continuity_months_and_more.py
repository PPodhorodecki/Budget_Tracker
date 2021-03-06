# Generated by Django 4.0 on 2022-01-07 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgettracker_app', '0004_category_expense_note_archive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='continuity_months',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='pay_month',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='pay_year',
        ),
        migrations.AddField(
            model_name='expense',
            name='continuity_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='continuity_step',
            field=models.IntegerField(null=True),
        ),
    ]
