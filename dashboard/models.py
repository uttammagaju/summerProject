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
    emp_email = models.CharField(max_length=50, blank=True )
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
    
class Milk(models.Model):
    milk_type = models.CharField(max_length=50)
    fat =  models.PositiveIntegerField()
    rate = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')

    class Meta:
        verbose_name = "Milk"
        verbose_name_plural = "Milk"
        ordering = ('id',)

    def __str__(self):
        return self.milk_type
    
class Farmer(models.Model):
    farmer_name = models.CharField(max_length=50)
    farmer_pwd = models.CharField(max_length=50)
    farmer_email = models.CharField(max_length=50)
    farmer_address = models.CharField(max_length=100)
    farmer_contact = models.PositiveBigIntegerField()
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')

    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
        ordering = ('id',)

    def __str__(self):
        return self.farmer_name
    
class Payment(models.Model):
    payment_date = models.DateField()
    amt = models.PositiveIntegerField()
    
