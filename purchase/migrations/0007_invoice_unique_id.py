# Generated by Django 4.0.3 on 2022-06-01 10:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0006_rename_invoice_description_invoicedescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
