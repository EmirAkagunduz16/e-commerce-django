# Generated by Django 5.2.1 on 2025-05-12 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='state',
        ),
    ]
