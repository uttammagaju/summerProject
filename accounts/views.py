from datetime import date
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy
from user.models import *
from .forms import LoginForm
from django.contrib.auth.views import LoginView


# Create your views here.
class LoginViews(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        role = form.instance.role
        print(role)
        if (
            form.instance.role == User.Role.EMPLOYEE
            or form.instance.role == User.Role.FARMER
        ):
            login(self.request, form.instance)
            return HttpResponse(" You are not a Admin")
        if form.instance.role == User.Role.ADMIN and form.instance.is_active:
            login(self.request, form.instance)
            self.request.session["admin_id"] = form.instance.id
            self.request.session["username"] = form.instance.username
            employees = EmployeeProfile.objects.all()

            for employee in employees:
                today = date.today()
                years_worked = today.year -employee.reg_date.year

                if years_worked >= 2:
                    employee.salary *= 1.1 #increase salary by 10%
                if years_worked >= 4:
                    employee.salary *= 1.15 #increase salary by 15%
                
                employee.save()
                
            return redirect(reverse_lazy("dashboard:home"))


class LogoutViews(FormView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect(reverse_lazy("accounts:login"))


class EmployeeLoginViews(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        if (
            form.instance.role == User.Role.ADMIN
            or form.instance.role == User.Role.FARMER
        ):
            login(self.request, form.instance)
            return HttpResponse(" You are not a employee")

        elif form.instance.role == User.Role.EMPLOYEE and form.instance.is_active:
            login(self.request, form.instance)
            employee = EmployeeProfile.objects.get(user_id=form.instance.id)
            self.request.session["employee_id"] = employee.id
            self.request.session["employee_name"] = employee.emp_name
            return redirect(reverse_lazy("employees:home"))


class EmployeeLogoutViews(FormView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect(reverse_lazy("accounts:employee-login"))
