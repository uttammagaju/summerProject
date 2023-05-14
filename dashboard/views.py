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

#Milk
class MilkListView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/milk/list.html'
    model = Milk

@login_required
def milkCreateView(request):
    n=''
    if request.method == "POST":
        fat = request.POST.get('fat') 
        fat_rate = request.POST.get('fat_rate')
        qty = request.POST.get('qty')
        date = request.POST.get('date')
        emp_id = request.POST.get('emp_id')
        emp = Employee.objects.get(id=emp_id)
        fatrate_id = request.POST.get('fatrate_id')
        fatrate = FatRate.objects.get(id=fatrate_id)
        farmer_id = request.POST.get('farmer_id')
        farmer = Farmer.objects.get(id=farmer_id)
        Milk.objects.create(fat = fat, fat_rate = fat_rate ,qty= qty, 
                        date = date,fatrate_id = fatrate, emp_id = emp, farmer_id = farmer)
        return redirect(reverse_lazy('dashboard:milk-list'))
    else:
        return render(request, "dashboard/milk/form.html",
                  {
                    'employees': Employee.objects.all(),
                    'fatrates' : FatRate.objects.all(),
                    'farmers'  : Farmer.objects.all()
                  }
                  )
    
@login_required
def milkUpdateView(request, pk):
    milk = Milk.objects.get(pk=pk)
    employees = Employee.objects.all()
    fatrates = FatRate.objects.all()
    farmers = Farmer.objects.all()
    if request.method == "POST":
        milk.fat = request.POST.get('fat') 
        milk.fat_rate = request.POST.get('fat_rate')
        milk.qty = request.POST.get('qty')
        milk.date = request.POST.get('date')
        milk.emp_id =  Employee.objects.get(pk=request.POST['emp_id'])
        milk.fatrate_id =  FatRate.objects.get(pk=request.POST['fatrate_id'])
        milk.farmer_id =  Farmer.objects.get(pk=request.POST['farmer_id'])
        milk.save()
        return redirect(reverse_lazy('dashboard:milk-list'))
    return render(request,'dashboard/milk/update_Form.html',
                  {'employees':employees,
                   'milk':milk,
                   'fatrates':fatrates,
                   'farmers': farmers,
                   })

@login_required
def milkDeleteView(request, pk):
    milk = Milk.objects.get(pk=pk)
    milk.delete()
    return HttpResponseRedirect(reverse('dashboard:milk-list'))

#commission
class CommissionListView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/commissions/list.html'
    model = Commission

@login_required
def commissionCreateView(request):
    n=''
    if request.method == "POST":
        commission_amt = request.POST.get('commission_amt') 
        commission_pay_date = request.POST.get('commission_pay_date')
        admin_id = request.POST.get('admin_id')
        admin = User.objects.get(id=admin_id)
        emp_id = request.POST.get('emp_id')
        emp = Employee.objects.get(id=emp_id)
        Commission.objects.create(commission_amt =commission_amt,commission_pay_date =commission_pay_date, emp_id = emp, admin_id=admin)
        return redirect(reverse_lazy('dashboard:commissions-list'))
    else:
        return render(request, "dashboard/commissions/form.html",
                  {
                    'employees': Employee.objects.all(),
                    'admins' : User.objects.all()
                  }
                  )
    
@login_required
def commissionUpdateView(request, pk):
    commissions = Commission.objects.get(pk=pk)
    employees = Employee.objects.all()
    admins = User.objects.all()
    if request.method == "POST":
        commissions.commission_amt = request.POST.get('Commission_amt') 
        commissions.commission_pay_date = request.POST.get('commission_pay_date')
        commissions.admin_id =  User.objects.get(pk=request.POST['admin_id'])
        commissions.emp_id =  Employee.objects.get(pk=request.POST['emp_id'])
        commissions.save()
        return redirect(reverse_lazy('dashboard:commissions-list'))
    return render(request,'dashboard/commissions/update_Form.html',
                  {'employees':employees,
                   'commission':commissions,
                   'admins':admins,
                   })

@login_required
def commissionDeleteView(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission.delete()
    return HttpResponseRedirect(reverse('dashboard:commissions-list'))

#Payment
class PaymentListView(LoginRequiredMixin,ListView):
    template_name = 'dashboard/payments/list.html'
    model = Payment

@login_required
def paymentCreateView(request):
    n=''
    if request.method == "POST":
        amt = request.POST.get('amt') 
        payment_date = request.POST.get('payment_date')
        admin_id = request.POST.get('admin_id')
        admin = User.objects.get(id=admin_id)
        farmer_id = request.POST.get('farmer_id')
        farmer = Farmer.objects.get(id=farmer_id)
        Payment.objects.create(amt =amt,payment_date =payment_date, admin_id=admin, farmer_id = farmer)
        return redirect(reverse_lazy('dashboard:payments-list'))
    else:
        return render(request, "dashboard/payments/form.html",
                  {
                    'farmers': Farmer.objects.all(),
                    'admins' : User.objects.all()
                  }
                  )
    
@login_required
def paymentUpdateView(request, pk):
    payments = Payment.objects.get(pk=pk)
    farmers = Farmer.objects.all()
    admins = User.objects.all()
    if request.method == "POST":
        payments.amt = request.POST.get('amt') 
        payments.payment_date = request.POST.get('payment_date')
        payments.admin_id =  User.objects.get(pk=request.POST['admin_id'])
        payments.farmer_id =  Farmer.objects.get(pk=request.POST['farmer_id'])
        payments.save()
        return redirect(reverse_lazy('dashboard:payments-list'))
    return render(request,'dashboard/payments/update_Form.html',
                  {'farmers':farmers,
                   'payment':payments,
                   'admins':admins,
                   })

@login_required
def paymentDeleteView(request, pk):
    payment = Payment.objects.get(pk=pk)
    payment.delete()
    return HttpResponseRedirect(reverse('dashboard:payments-list'))