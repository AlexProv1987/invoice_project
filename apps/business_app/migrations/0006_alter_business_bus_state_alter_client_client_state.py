# Generated by Django 4.1.3 on 2022-12-15 19:26

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "business_app",
            "0005_alter_business_bus_city_alter_business_bus_email_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="business",
            name="bus_state",
            field=localflavor.us.models.USStateField(
                max_length=2, verbose_name="State"
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="client_state",
            field=localflavor.us.models.USStateField(
                max_length=2, verbose_name="State"
            ),
        ),
    ]