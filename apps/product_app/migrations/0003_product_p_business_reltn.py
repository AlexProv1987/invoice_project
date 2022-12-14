# Generated by Django 4.1.3 on 2022-12-13 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("business_app", "0004_alter_client_client_city"),
        ("product_app", "0002_product_p_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="p_business_reltn",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="business_app.business",
            ),
            preserve_default=False,
        ),
    ]
