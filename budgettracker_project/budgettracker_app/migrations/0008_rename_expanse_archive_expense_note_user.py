# Generated by Django 4.0 on 2022-01-13 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('budgettracker_app', '0007_alter_category_user_alter_expense_user_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archive',
            old_name='expanse',
            new_name='expense',
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
