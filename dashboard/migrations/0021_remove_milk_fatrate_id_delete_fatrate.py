# Generated by Django 4.1.3 on 2023-05-15 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_remove_fatrate_type_of_milk_remove_milk_fat_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milk',
            name='fatrate_id',
        ),
        migrations.DeleteModel(
            name='FatRate',
        ),
    ]
