# Generated by Django 4.2.5 on 2024-07-19 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff_firewall", "0005_alter_fwstaff_instance_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fwstaff",
            name="firewall_uuid",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name="fwstaff",
            name="instance_id",
            field=models.CharField(max_length=256, null=True),
        ),
    ]
