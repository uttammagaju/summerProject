from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import login_required 
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

#Farmer
class FarmerListView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/farmers/list.html'
    model = Farmer

@login_required
def farmerCreateView(request):
    n=''
    if request.method == "POST":
        farmer_name = request.POST.get('farmer_name') 
        farmer_pwd = request.POST.get('farmer_pwd')
        farmer_email = request.POST.get('farmer_email')
        farmer_address = request.POST.get('farmer_address')
        farmer_contact = request.POST.get('farmer_contact')
        admin_id = request.POST.get('admin_id')
        admin = User.objects.get(id=admin_id)
        Farmer.objects.create(farmer_name = farmer_name, farmer_pwd = farmer_pwd ,farmer_email= farmer_email, 
                        farmer_address = farmer_address, farmer_contact = farmer_contact, admin_id = admin)
        return redirect(reverse_lazy('dashboard:farmers-list'))
    else:
        return render(request, "dashboard/farmers/form.html",
                  {
                    'admins':User.objects.all(),
                  }
                  )
    
@login_required
def farmerUpdateView(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    admins = User.objects.all()
    if request.method == "POST":
        farmer.farmer_email = request.POST['farmer_email']
        farmer.farmer_pwd = request.POST['farmer_pwd']
        farmer.farmer_name = request.POST['farmer_name']
        farmer.farmer_contact = request.POST['farmer_contact']
        farmer.farmer_address = request.POST['farmer_address']
        farmer.admin_id = User.objects.get(pk=request.POST['admin_id'])
        farmer.save()
        return redirect(reverse_lazy('dashboard:farmers-list'))
    return render(request,'dashboard/farmers/update_Form.html',
                  {'farmer':farmer,
                   'admins':admins
                   })

@login_required
def farmerDeleteView(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    farmer.delete()
    return HttpResponseRedirect(reverse('dashboard:farmers-list'))

#Milk
class FatRateListView(ListView):
    template_name = 'dashboard/fatrates/list.html'
    model = FatRate

@login_required
def fatrateCreateView(request):
    n=''
    if request.method == "POST":
        type_of_milk = request.POST.get('type_of_milk') 
        rate = request.POST.get('rate')
        rate_set_date = request.POST.get('rate_set_date')
        admin_id = request.POST.get('admin_id')
        admin = User.objects.get(id=admin_id)
        is_published = request.POST.get('is_published',False) == 'True'
        FatRate.objects.create(type_of_milk = type_of_milk, rate = rate , rate_set_date= rate_set_date, admin_id = admin, is_published = is_published)
        return redirect(reverse_lazy('dashboard:fatrates-list'))
    else:
        return render(request, "dashboard/fatrates/form.html",
                  {
                    'admins':User.objects.all(),
                  }
                  )

# @login_required
# def fatrateUpdateView(request, pk):
#     fatrates = FatRate.objects.get(pk=pk)
#     admins = User.objects.all()
#     if request.method == "POST":
#         fatrates.type_of_milk= request.POST['type_of_milk']
#         fatrates.rate = request.POST['rate']
#         fatrates.rate_set_date = request.POST['rate_set_date']
#         fatrates.emp_contact = request.POST['emp_contact']
#         fatrates.admin_id = User.objects.get(pk=request.POST['admin_id'])
#         fatrates.is_published = request.POST['is_published',False] == 'True'
#         fatrates.save()
#         return redirect(reverse_lazy('dashboard:fatrates-list'))
#     return render(request,'dashboard/fatrates/update_Form.html',
#                   {'fatrates':fatrates,
#                    'admins':admins,
#                    'rate_set_date':fatrates.rate_set_date.isoformat()
#                    })

@login_required
def fatrateDeleteView(request, pk):
    fatrate = FatRate.objects.get(pk=pk)
    fatrate.delete()
    return HttpResponseRedirect(reverse('dashboard:fatrates-list'))