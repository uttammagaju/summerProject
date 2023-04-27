from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import login_required 
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from . models import *

User = get_user_model()
# Create your views here.


class DashboardHomeView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/index.html"


#Admin
# class AdminListView(ListView):
#     template_name = 'dashboard/admins/list.html'
#     model = Admin

# def adminCreateView(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('full_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         admin_pwd = request.POST.get('admin_pwd')
#         data = Admin(full_name = full_name, username = username, 
#                      email = email, admin_pwd = admin_pwd)
#         data.save()
#         return redirect(reverse_lazy('dashboard:admins-list'))
#     else: 
#          return render(request, "dashboard/admins/form.html")


# class AdminDeleteView(DeleteView):
#     model = Admin
#     success_url = reverse_lazy('dashboard:admins-list')


#Employee
class EmployeeListView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/employees/list.html'
    model = Employee

@login_required
def employeeCreateView(request):
    n=''
    if request.method == "POST":
        emp_email = request.POST.get('emp_email') 
        emp_pwd = request.POST.get('emp_pwd')
        emp_name = request.POST.get('emp_name')
        emp_contact = request.POST.get('emp_contact')
        salary = request.POST.get('salary')
        reg_date= request.POST.get('reg_date')
        admin_id = request.POST.get('admin_id')
        admin = User.objects.get(id=admin_id)
        Employee.objects.create(emp_email = emp_email, emp_pwd = emp_pwd ,emp_name= emp_name, 
                        emp_contact = emp_contact, salary = salary, reg_date = reg_date,
                        admin_id = admin)
        return redirect(reverse_lazy('dashboard:employees-list'))
    else:
        return render(request, "dashboard/employees/form.html",
                  {
                    'admins':User.objects.all(),
                  }
                  )
@login_required
def employeeUpdateView(request, pk):
    employee = Employee.objects.get(pk=pk)
    admins = User.objects.all()
    if request.method == "POST":
        employee.emp_email = request.POST['emp_email']
        employee.emp_pwd = request.POST['emp_pwd']
        employee.emp_name = request.POST['emp_name']
        employee.emp_contact = request.POST['emp_contact']
        employee.salary = request.POST['salary']
        employee.admin_id = User.objects.get(pk=request.POST['admin_id'])
        employee.reg_date = request.POST['reg_date']
        employee.save()
        return redirect(reverse_lazy('dashboard:employees-list'))
    return render(request,'dashboard/employees/update_Form.html',
                  {'employee':employee,
                   'admins':admins,
                   'reg_date':employee.reg_date.isoformat()
                   })
@login_required
def employeeDeleteView(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return HttpResponseRedirect(reverse('dashboard:employees-list'))