# Generated by Django 2.2 on 2019-04-24 12:49

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_address'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='address',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
