from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYEE = "EMPLOYEE", "Employee"
        FARMER = "FARMER", "Farmer"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.EMPLOYEE)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEE)


class Employee(User):
    base_role = User.Role.EMPLOYEE
    objects = EmployeeManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for employees"


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile", null=True
    )
    emp_email = models.CharField(max_length=50, blank=True, null=True)
    emp_pwd = models.CharField(max_length=255, blank=True, null=True)
    emp_name = models.CharField(max_length=50, blank=True, null=True)
    emp_contact = models.PositiveBigIntegerField(blank=True, null=True)
    salary = models.PositiveIntegerField(blank=True, null=True)
    reg_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    admin_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admin_employee_profiles",
        blank=False,
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ("id",)

    def __str__(self):
        return self.emp_name


class FarmerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.FARMER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.FARMER)


class Farmer(User):
    base_role = User.Role.FARMER
    objects = FarmerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "only for farmers"


class FarmerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="farmer", null=True
    )
    farmer_name = models.CharField(max_length=50)
    farmer_pwd = models.CharField(max_length=50)
    farmer_email = models.CharField(max_length=50)
    farmer_address = models.CharField(max_length=100)
    farmer_contact = models.PositiveBigIntegerField()
    admin_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_farmer", blank=False
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
        ordering = ("id",)

    def __str__(self):
        return self.farmer_name
