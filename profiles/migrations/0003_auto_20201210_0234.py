# Generated by Django 3.1.3 on 2020-12-09 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20201201_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('accepted', 'accepted')], max_length=10),
        ),
    ]
