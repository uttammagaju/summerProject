from django.db import models
from django.contrib.auth.models import User
from user.models import *

# Create your models here.


class Commission(models.Model):
    commission_amt = models.PositiveIntegerField(null=True)
    commission_pay_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='unpaid')
    admin_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commission", null=True
    )
    emp_id = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="commission",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"
        ordering = ("id",)

    def __str__(self):
        return self.Commission_amt


# class FatRate(models.Model):
#     rate = models.PositiveBigIntegerField()
#     rate_set_date = models.DateField(blank=True, null=True)
#     admin_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='fatrate', blank=False)
#     is_published = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "FatRate"
#         verbose_name_plural = "FatRates"
#         ordering = ('id',)

#     def __int__(self):
#         return self.rate


class Milk(models.Model):
    fat = models.FloatField()
    qty = models.FloatField()
    rate = models.PositiveIntegerField(null=True)
    date = models.DateField(null=True, blank=True)
    emp_id = models.ForeignKey(
        EmployeeProfile, on_delete=models.CASCADE, related_name="milk_emp", blank=True
    )
    # fatrate_id = models.ForeignKey(FatRate, on_delete=models.CASCADE, related_name='milk', blank=True, null=True)
    farmer_id = models.ForeignKey(FarmerProfile,on_delete=models.CASCADE,related_name="milk_farmer",blank=True,null=True)

    class Meta:
        verbose_name = "Milk"
        verbose_name_plural = "Milk"
        ordering = ("id",)

    def __str__(self):
        return self.fat


class Payment(models.Model):
    amt = models.PositiveIntegerField()
    payment_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='unpaid')
    emp_id = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="payment",
        blank=True,
        null=True,
    )
    admin_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payment_admin",
        blank=True,
        null=True
    )
    farmer_id = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE,
        related_name="payment_farmer",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ("id",)

    def __str__(self):
        return self.amt
