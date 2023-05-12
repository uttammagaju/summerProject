# Generated by Django 4.1.7 on 2023-05-05 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0009_alter_employee_admin_id_alter_farmer_admin_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('id',), 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.RemoveField(
            model_name='milk',
            name='rate',
        ),
        migrations.AddField(
            model_name='payment',
            name='admin_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='farmer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='dashboard.farmer'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='admin_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='milk',
            name='emp_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='milk', to='dashboard.employee'),
        ),
        migrations.CreateModel(
            name='FatRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveBigIntegerField(default='15')),
                ('rate_set_date', models.DateField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fatrate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FatRate',
                'verbose_name_plural': 'FatRates',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Commission_amt', models.PositiveIntegerField(null=True)),
                ('commission_pay_date', models.PositiveIntegerField(blank=True)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commission', to=settings.AUTH_USER_MODEL)),
                ('employee_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='commission', to='dashboard.employee')),
            ],
            options={
                'verbose_name': 'Commission',
                'verbose_name_plural': 'Commissions',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='milk',
            name='fatrate_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='milk', to='dashboard.fatrate'),
        ),
    ]