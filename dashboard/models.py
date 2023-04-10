from django.db import models

# Create your models here.
class Admin(models.Model):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    admin_pwd = models.CharField(max_length=50)

    class Meta:
        verbose_name="Admin"
        verbose_name_plural = "Admins"
        ordering = ('id',)

    def __str__(self):
        return self.full_name

class Employee(models.Model):
    emp_email = models.CharField(max_length=50)
    emp_pwd = models.  CharField(max_length=255)
    emp_name = models.CharField(max_length=50)
    emp_contact = models.PositiveBigIntegerField(max_length=10)
    salary = models.PositiveIntegerField(max_length=20)
    reg_date = models.DateField()
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='employee')
    commission_amt = models.PositiveIntegerField(max_length=50)

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
    date = models.DateField()
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
    farmer_contact = models.PositiveBigIntegerField(max_length=10)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='admin')

    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
        ordering = ('id',)

    def __str__(self):
        return self.farmer_name
    
class Payment(models.Model):
    payment_date = models.DateField()
    amt = models.PositiveIntegerField()
    
