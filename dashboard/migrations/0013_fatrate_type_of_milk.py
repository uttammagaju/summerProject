# Generated by Django 4.1.7 on 2023-05-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0012_remove_milk_milk_type_alter_employee_emp_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="fatrate",
            name="type_of_milk",
            field=models.TextField(max_length=50, null=True),
        ),
    ]
