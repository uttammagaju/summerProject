# Generated by Django 4.1.7 on 2023-04-24 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_employee_commission_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='reg_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milk',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]