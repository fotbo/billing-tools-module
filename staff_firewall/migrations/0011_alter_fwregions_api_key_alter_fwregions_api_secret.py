# Generated by Django 4.2.5 on 2024-06-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_firewall", "0010_alter_fwregions_api_key_alter_fwregions_api_secret"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fwregions",
            name="api_key",
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name="fwregions",
            name="api_secret",
            field=models.BinaryField(),
        ),
    ]
