# Generated by Django 4.0.3 on 2022-06-01 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_rename_supplier_contac_name_customers_supplier_contact_name_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='invoice_description',
            new_name='InvoiceDescription',
        ),
    ]
