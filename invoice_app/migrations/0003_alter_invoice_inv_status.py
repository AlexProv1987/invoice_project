# Generated by Django 4.1.3 on 2022-12-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoice_app", "0002_alter_invoice_inv_paid_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="inv_status",
            field=models.IntegerField(
                choices=[(1, "Generated"), (2, "Billed"), (3, "Paid")]
            ),
        ),
    ]