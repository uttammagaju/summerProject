# Generated by Django 4.1.7 on 2023-04-14 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_alter_employee_emp_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="emp_email",
            field=models.CharField(max_length=50),
        ),
    ]
