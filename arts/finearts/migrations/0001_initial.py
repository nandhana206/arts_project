# Generated by Django 4.2.17 on 2024-12-11 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('admission_number', models.CharField(max_length=15, unique=True)),
                ('department', models.CharField(max_length=50)),
            ],
        ),
    ]
