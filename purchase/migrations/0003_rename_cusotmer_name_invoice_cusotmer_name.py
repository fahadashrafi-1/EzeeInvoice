# Generated by Django 3.2.5 on 2021-11-24 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20211123_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='cusotmer_Name',
            new_name='cusotmer_name',
        ),
    ]
