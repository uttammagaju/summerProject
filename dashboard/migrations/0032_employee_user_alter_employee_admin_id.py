# Generated by Django 4.1.7 on 2023-05-28 02:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dashboard", "0031_payment_emp_id_alter_commission_admin_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="admin_id",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="admin_employee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]