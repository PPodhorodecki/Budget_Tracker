# Generated by Django 4.0 on 2022-01-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=16, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=64)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('account_created', models.DateField()),
                ('last_log', models.DateTimeField(null=True)),
            ],
        ),
    ]