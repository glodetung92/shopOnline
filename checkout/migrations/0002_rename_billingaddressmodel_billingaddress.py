# Generated by Django 4.1.3 on 2022-12-08 09:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillingAddressModel',
            new_name='BillingAddress',
        ),
    ]