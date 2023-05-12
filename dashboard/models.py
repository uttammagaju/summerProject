from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class Admin(models.Model):
#     full_name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     admin_pwd = models.CharField(max_length=50)

#     class Meta:
#         verbose_name="Admin"
#         verbose_name_plural = "Admins"
#         ordering = ('id',)

#     def __str__(self):
#         return self.full_name

class Employee(models.Model):
    emp_email = models.CharField(max_length=50, blank=True , null=True)
    emp_pwd = models.  CharField(max_length=255, blank=True)
    emp_name = models.CharField(max_length=50, blank=True)
    emp_contact = models.PositiveBigIntegerField(blank=True)
    salary = models.PositiveIntegerField(blank=True)
    reg_date = models.DateField(null=True, blank=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee', blank=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ('id',)

    def __str__(self):
        return self.emp_name
    
class Commission(models.Model):
    commission_amt = models.PositiveIntegerField(null=True)
    commission_pay_date = models.DateField()
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission')
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='commission', blank=True)

    class Meta:
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"
        ordering = ('id',)

    def __str__(self):
        return self.Commission_amt

class FatRate(models.Model):
    type_of_milk = models.TextField(max_length=50, null=True)
    rate = models.PositiveBigIntegerField()
    rate_set_date = models.DateField(blank=True, null=True)
    admin_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='fatrate', blank=False)  
    is_published = models.BooleanField(default=False) 

    class Meta:
        verbose_name = "FatRate"
        verbose_name_plural = "FatRates"
        ordering = ('id',)

    def __str__(self):
        return self.type_of_milk

class Farmer(models.Model):
    farmer_name = models.CharField(max_length=50)
    farmer_pwd = models.CharField(max_length=50)
    farmer_email = models.CharField(max_length=50)
    farmer_address = models.CharField(max_length=100)
    farmer_contact = models.PositiveBigIntegerField()
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer', blank=True,null=True)

    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
        ordering = ('id',)

    def __str__(self):
        return self.farmer_name

class Milk(models.Model):
    fat =  models.FloatField()
    fat_rate = models.PositiveIntegerField(null=True)
    qty = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='milk', blank=True)
    fatrate_id = models.ForeignKey(FatRate, on_delete=models.CASCADE, related_name='milk', blank=True, null=True)
    farmer_id = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='milk', blank=True)

    class Meta:
        verbose_name = "Milk"
        verbose_name_plural = "Milk"
        ordering = ('id',)

    def __Float__(self):
        return self.fat
    
class Payment(models.Model):
    payment_date = models.DateField()
    amt = models.PositiveIntegerField()
    farmer_id = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment', blank=True, null=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ("id",)

    def __str__(self):
        return self.amt