from accounts.forms import User
from django.contrib.auth.backends import BaseBackend
from dashboard.models import Employee, Farmer


class EmployeeFarmerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the provided username is an employee email
        try:
            employee = Employee.objects.get(emp_email=username)
            user = employee.user
            user_type = "employee"
        except Employee.DoesNotExist:
            # If the provided username is not an employee email, check if it's a farmer email
            try:
                farmer = Farmer.objects.get(farmer_email=username)
                user = farmer.user
                user_type = "farmer"
            except Farmer.DoesNotExist:
                return None

        if user.check_password(password):
            user.user_type = user_type  # Assign the user_type attribute
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
