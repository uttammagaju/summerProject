from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy
from dashboard.models import *
from .forms import LoginForm


# Create your views here.
class LoginViews(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.instance)
        self.request.session["admin_id"] = form.instance.id
        self.request.session["username"] = form.instance.username
        return redirect(reverse_lazy("dashboard:home"))


class LogoutViews(FormView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect(reverse_lazy("accounts:login"))


# employee
def employeeLogin(request):
    if request.method == "POST":
        emp_email = request.POST["email"]
        emp_pwd = request.POST["password"]
        employee = Employee.authenticate_employee(emp_email, emp_pwd)

        if employee is not None:
            print(employee.emp_email)
            request.session["employee_id"] = employee.id
            request.session["employee_name"] = employee.emp_name
            return redirect(reverse_lazy("employees:home"))
        elif employee is None:
            return HttpResponse(" You are not a employee")
        else:
            return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")

def employeeLogout(request):
    logout(request)
    return redirect(reverse_lazy('accounts:employee-login'))

# #farmer
# def farmerLogin(request):
#     if request.method == 'POST':
#         farmer_email =request.POST['email']
#         farmer_pwd = request.POST['password']
#         farmer = Farmer.authenticate_farmer(farmer_email, farmer_pwd)

#         if farmer is not None:
#             return redirect(reverse_lazy('dashboard:payments-create'))
        
#         else: 
#             return render(request, 'accounts/login.html')
#     return render(request, 'accounts/login.html')