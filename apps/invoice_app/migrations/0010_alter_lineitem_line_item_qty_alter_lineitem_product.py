# Generated by Django 4.1.3 on 2022-12-13 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0002_product_p_is_active"),
        ("invoice_app", "0009_alter_invoice_inv_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lineitem",
            name="line_item_qty",
            field=models.PositiveBigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name="lineitem",
            name="product",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="product_app.product",
            ),
        ),
    ]
