# Generated by Django 4.1.7 on 2023-05-15 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_alter_milk_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milk',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
