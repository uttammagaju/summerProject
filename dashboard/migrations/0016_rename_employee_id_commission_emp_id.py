# Generated by Django 4.1.7 on 2023-05-12 15:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0015_alter_milk_fat"),
    ]

    operations = [
        migrations.RenameField(
            model_name="commission",
            old_name="employee_id",
            new_name="emp_id",
        ),
    ]
