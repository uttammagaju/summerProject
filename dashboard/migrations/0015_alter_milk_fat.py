# Generated by Django 4.1.7 on 2023-05-12 01:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0014_alter_fatrate_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="milk",
            name="fat",
            field=models.FloatField(),
        ),
    ]
