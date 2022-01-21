# Generated by Django 4.0 on 2022-01-21 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('budgettracker_app', '0015_rename_continuity_amount_expense_exp_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='paid_date',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('paid', models.DateField()),
                ('category', models.CharField(max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
