# Generated by Django 4.1.7 on 2023-05-12 15:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0016_rename_employee_id_commission_emp_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="commission",
            old_name="Commission_amt",
            new_name="commission_amt",
        ),
    ]
