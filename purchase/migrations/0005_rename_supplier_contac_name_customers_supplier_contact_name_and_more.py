# Generated by Django 4.0.3 on 2022-05-23 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_alter_customers_mobile_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='supplier_Contac_Name',
            new_name='supplier_Contact_Name',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='vat',
        ),
    ]
