# Generated by Django 4.1.3 on 2023-02-15 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0006_alter_product_p_instock"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["p_name"], name="product_app_p_name_cb7a76_idx"),
        ),
    ]
