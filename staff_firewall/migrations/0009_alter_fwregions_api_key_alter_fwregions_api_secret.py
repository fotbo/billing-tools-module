# Generated by Django 4.2.5 on 2024-06-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_firewall", "0008_fwstaff_enabled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fwregions",
            name="api_key",
            field=models.BinaryField(max_length=550),
        ),
        migrations.AlterField(
            model_name="fwregions",
            name="api_secret",
            field=models.BinaryField(max_length=550),
        ),
    ]
