# Generated by Django 4.2.5 on 2024-07-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_firewall", "0002_fwstaff_instance_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fwstaff",
            name="instance_id",
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
