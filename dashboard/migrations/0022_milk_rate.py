# Generated by Django 4.1.3 on 2023-05-15 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_remove_milk_fatrate_id_delete_fatrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='milk',
            name='rate',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
