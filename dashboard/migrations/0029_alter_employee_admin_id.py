# Generated by Django 4.1.7 on 2023-05-19 05:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dashboard", "0028_alter_milk_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="admin_id",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="employee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
