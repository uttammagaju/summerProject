# Generated by Django 4.1.7 on 2023-05-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_farmerprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="farmerprofile",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
