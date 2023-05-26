from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import login_required 
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
import re

from .forms import *
from . models import *

User = get_user_model()
# request.session['admin_id'] = User.id
# Create your views here.


# class DashboardHomeView(LoginRequiredMixin,TemplateView):
#     template_name = "dashboard/index.html"

@login_required(login_url= '/dashboard/accounts/login')
def dashboardHomeView(request):
    #count employee
    employee_count = Employee.objects.count()
    #callculate the total milk collected today
    total_milk_collected = Milk.objects.filter(date = date.today()).aggregate(total_qty=models.Sum('qty'))['total_qty']
    return render(request,"dashboard/index.html",{'employee_count' : employee_count,'total_milk_collected': total_milk_collected})


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
@login_required(login_url= '/dashboard/accounts/login')
def employeeListView(request):
    employees = Employee.objects.all()
    return render(request,"dashboard/employees/list.html",{'employees': employees})


@login_required(login_url= '/dashboard/accounts/login')
def employeeCreateView(request):
    # request.session['admin_id']=User.id
    n=''
    if request.method == "POST":
        emp_email = request.POST.get('emp_email') 
        emp_pwd = request.POST.get('emp_pwd')
        emp_name = request.POST.get('emp_name')
        emp_contact = request.POST.get('emp_contact')
        salary = request.POST.get('salary')
        reg_date= request.POST.get('reg_date')
        admin_id = User.objects.get(id=request.session.get('admin_id'))
        

        errors = {}
        #perform Validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not emp_email:
            errors['emp_email'] = 'email field is requied.'
        elif not re.match(email_pattern,emp_email):
            errors['emp_email'] = 'email is not valid.'
        elif Employee.objects.filter(emp_email=emp_email).exists():
            errors['emp_email'] = 'email is already taken.'
        
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
        if not emp_pwd:
            errors['emp_pwd'] = 'password field is required.'
        elif not re.match(password_pattern , emp_pwd):
            errors['emp_pwd'] = 'Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit.'

        name_pattern = r'^[A-Za-z\s]+$'
        if not emp_name:
            errors['emp_name'] = 'name field is required.'
        elif not re.match(name_pattern,emp_name):
            errors['emp_name'] = 'Invalid name'

        contact_pattern = r'^98\d{8}$'
        if not emp_contact:
            errors['emp_contact'] = 'contact field is required.'
        elif not re.match(contact_pattern,emp_contact):
            errors['emp_contact'] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'

        salary_pattern = r'^[1-9]\d*(\.\d+)?$'
        if not salary:
            errors['salary'] = 'salary field is required.'
        elif not re.match(salary_pattern, salary):
            errors['salary'] = 'Invalid salary format. It must be a number.'
        elif float(salary)>15000:
            errors['salary'] = 'Invalid salary. Maximum salary is 15000.'

        # reg_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not reg_date:
            errors['reg_date'] = 'date filed is required.'
        else:
            try: 
                r_date = date.fromisoformat(reg_date)
                if r_date > date.today():
                    errors['reg_date'] = 'Selected date cannot be in future.' 
            except ValueError:
                errors['reg_date'] = 'Invalid date format.'
        
              
        if errors:
            return render(request, 'dashboard/employees/form.html', {'errors':errors,'emp_email':emp_email, 'emp_name': emp_name, 'emp_pwd': emp_pwd, 'emp_name':emp_name, 'emp_contact':emp_contact, 'salary':salary, 'reg_date':reg_date})

        else:
            Employee.objects.create(emp_email = emp_email, emp_pwd = emp_pwd ,emp_name= emp_name, 
                            emp_contact = emp_contact, salary = salary, reg_date = reg_date,
                            admin_id = admin_id)
            # User.objects.create_user(username = emp_name, email = emp_email, password= emp_pwd)
        return redirect(reverse_lazy('dashboard:employees-list'))
    else:
        return render(request, "dashboard/employees/form.html",
                  {
                    'admins':User.objects.all(),
                  }
                  )
    
@login_required(login_url= '/dashboard/accounts/login')
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

@login_required(login_url= '/dashboard/accounts/login')
def employeeDeleteView(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return HttpResponseRedirect(reverse('dashboard:employees-list'))

#Farmer
@login_required(login_url= '/dashboard/accounts/login')
def farmerListView(request):
    farmers = Farmer.objects.all()
    return render(request,"dashboard/farmers/list.html",{'farmers': farmers}) 

@login_required(login_url= '/dashboard/accounts/login')
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

        errors = {}
        #perform Validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not farmer_email:
            errors['farmer_email'] = 'email field is requied.'
        elif not re.match(email_pattern,farmer_email):
            errors['farmer_email'] = 'email is not valid.'
        elif Farmer.objects.filter(farmer_email=farmer_email).exists():
            errors['farmer_email'] = 'email is already taken.'
        
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
        if not farmer_pwd:
            errors['farmer_pwd'] = 'email field is required.'
        elif not re.match(password_pattern , farmer_pwd):
            errors['farmer_pwd'] = 'Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit.'

        name_pattern = r'^[A-Za-z\s]+$'
        if not farmer_name:
            errors['farmer_name'] = 'name field is required.'
        elif not re.match(name_pattern,farmer_name):
            errors['farmer_name'] = 'Invalid name'

        contact_pattern = r'^98\d{8}$'
        if not farmer_contact:
            errors['farmer_contact'] = 'contact field is required.'
        elif not re.match(contact_pattern,farmer_contact):
            errors['farmer_contact'] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'

        address_pattern = r'^\d+\s+([A-Za-z]+\s?)+,\s*\w+,\s*\w+\s*\d*$'
        if not farmer_address:
            errors['farmer_address'] = 'address field is required.'
        elif len(farmer_address) <5 :
            errors['farmer_address'] = 'Address must contain 5 letter'

        if not admin_id:
                    errors['admin_id'] = 'Select  the Admin '

        if errors:
            return render(request,'dashboard/farmers/form.html',{'errors':errors,'farmer_email':farmer_email,'farmer_pwd':farmer_pwd,'farmer_name':farmer_name,
                                                                'farmer_contact':farmer_contact,'farmer_address':farmer_address,'admin_id':admin_id})
        
        else:
            Farmer.objects.create(farmer_name = farmer_name, farmer_pwd = farmer_pwd ,farmer_email= farmer_email, 
                            farmer_address = farmer_address, farmer_contact = farmer_contact, admin_id = admin)
        return redirect(reverse_lazy('dashboard:farmers-list'))
    else:
        return render(request, "dashboard/farmers/form.html",
                  {
                    'admins':User.objects.all(),
                  }
                  )
    
@login_required(login_url= '/dashboard/accounts/login')
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

@login_required(login_url= '/dashboard/accounts/login')
def farmerDeleteView(request, pk):
    farmer = Farmer.objects.get(pk=pk)
    farmer.delete()
    return HttpResponseRedirect(reverse('dashboard:farmers-list'))

# #Fatrate
# class FatRateListView(ListView):
#     template_name = 'dashboard/fatrates/list.html'
#     model = FatRate

# @login_required
# def fatrateCreateView(request):
#     n=''
#     if request.method == "POST":
#         rate = request.POST.get('rate')
#         rate_set_date = request.POST.get('rate_set_date')
#         admin_id = request.POST.get('admin_id')
#         admin = User.objects.get(id=admin_id)
#         is_published = request.POST.get('is_published',False) == 'True'
#         FatRate.objects.create( rate = rate , rate_set_date= rate_set_date, admin_id = admin, is_published = is_published)
#         return redirect(reverse_lazy('dashboard:fatrates-list'))
#     else:
#         return render(request, "dashboard/fatrates/form.html",
#                   {
#                     'admins':User.objects.all(),
#                   }
#                   )

# @login_required
# def fatrateUpdateView(request, pk):
#     fatrates = FatRate.objects.get(pk=pk)
#     admins = User.objects.all()
#     if request.method == "POST":
#         fatrates.rate = request.POST['rate']
#         fatrates.rate_set_date = request.POST['rate_set_date']
#         fatrates.admin_id = User.objects.get(pk=request.POST['admin_id'])
#         fatrates.is_published = request.POST['is_published',False] == 'True'
#         fatrates.save()
#         return redirect(reverse_lazy('dashboard:fatrates-list'))
#     return render(request,'dashboard/fatrates/update_Form.html',
#                   {'fatrates':fatrates,
#                    'admins':admins,
#                    'rate_set_date':fatrates.rate_set_date.isoformat()
#                    })

# @login_required
# def fatrateDeleteView(request, pk):
#     fatrate = FatRate.objects.get(pk=pk)
#     fatrate.delete()
#     return HttpResponseRedirect(reverse('dashboard:fatrates-list'))

#Milk
@login_required(login_url= '/dashboard/accounts/login')
def milkListView(request):
    milks = Milk.objects.all()
    return render(request, 'dashboard/milk/list.html',{'milks':milks})
  



# def milkCreateView(request):
#     n=''
#     if request.method == "POST":
#         fat = request.POST.get('fat') 
#         qty = request.POST.get('qty')
#         date_str = request.POST.get('date')
#         emp_id = request.POST.get('emp_id')
#         if emp_id:
#             emp = Employee.objects.get(id=emp_id)
#         else:
#             return HttpResponse("Please select an employee")
#         farmer_id = request.POST.get('farmer_id')
#         if farmer_id:
#             farmer = Farmer.objects.get(id=farmer_id)
#         else:
#             return HttpResponse("Please select an farmer")
        
        
#         fatrate=''
#         errors ={}
#         #perform validation
#         if emp is '':
#             HttpResponse("please select employee")

#         if not fat:
#             errors['fat'] ='Fat field is required.'
#         elif float(fat)<1:
#             errors['fat'] ='Fat should be negative.'
#         elif float(fat)>15:
#             errors['fat'] ='Fat should be less than 15.'
            

#         if not qty:
#             errors['qty']='Quantity field is required.'
#         elif float(qty)<1:
#             errors['qty']='Quantity field must be greater than 1 or positive'
#         elif float(qty)>=1 and float(qty)<=20:
#             fatrate=14.0
#         elif float(qty)>20 and float(qty)<=50:
#             fatrate=15.0
#         elif float(qty)>50 and float(qty)<=100:
#             fatrate=16.0
#         elif float(qty)>150:
#             fatrate=20.0
        
#         if not date_str:
#             errors['date']='Date field is required'
#         else:
#             try: 
#                 milk_date = date.fromisoformat(date_str)
#                 if milk_date > date.today():
#                     errors['date'] = 'Selected date cannot be in future.' 
#             except ValueError:
#                 errors['date'] = 'Invalid date format.'

#         if not emp_id:
#             errors['emp_id'] = 'Selected the employee'

#         if not farmer_id:
#             errors['farmer_id']= 'Selected the farmer'

#         if errors:
#             return render(request,"dashboard/milk/form.html",{'errors': errors,'fat': fat, 'qty': qty,'date': date_str,'emp_id' : emp, 'farmer_id': farmer})
        
#         else:
#             admin = User.objects.get(id=request.session.get('admin_id')) 
#             #calculate the payment amt
#             amt =float(fat) * float(qty) * float(fatrate)

#             #create milk object
#             Milk.objects.create(fat = fat, qty= qty, date = date_str, rate = fatrate, emp_id = emp, farmer_id = farmer)
#             #calculate commission
#             fill_date = date.today()

#             if Commission.objects.filter(emp_id=emp_id ,commission_pay_date =fill_date).exists():
#                 total_quantity = Milk.objects.filter(emp_id=emp_id, date=fill_date).aggregate(total_qty=models.Sum('qty'))['total_qty']
#                 if total_quantity <=500:
#                     commission_rate = 0.1
#                     Commission.objects.filter(emp_id=emp_id).update(commission_amt=total_quantity*commission_rate)

#                 elif total_quantity > 500:
#                     commission_rate = 0.2
#                     Commission.objects.filter(emp_id=emp_id).update(commission_amt=total_quantity*commission_rate)
            
#             else:
#                 if not  Commission.objects.filter(emp_id=emp_id ,commission_pay_date =fill_date).exists():
#                     if float(qty) <= 500:
#                         commission_rate = 0.1
#                     elif float(qty) >= 1000:
#                         commission_rate = 0.2
#                     first_amt = float(qty) * commission_rate
#                     Commission.objects.create(commission_amt = first_amt, commission_pay_date = date_str ,emp_id = emp, admin_id = admin)

           
#                 # pay_date = Commission.objects.get('commission_pay_date')
#                 # if Commission.object.filter(fill_date = pay_date):
#                 #     f


#             #create payment object
#             Payment.objects.create(amt = amt, admin_id = admin ,payment_date = date_str, farmer_id = farmer, )
#             return redirect(reverse_lazy('dashboard:milk-list'))
#     else:
#         return render(request, "dashboard/milk/form.html",
#                   {
#                     'employees': Employee.objects.all(),
#                     # 'fatrates' : FatRate.objects.all(),
#                     'farmers'  : Farmer.objects.all()
#                   }
#                   )
    
@login_required(login_url= '/dashboard/accounts/login')
def milkUpdateView(request, pk):
    milk = Milk.objects.get(pk=pk)
    employees = Employee.objects.all()
    # fatrates = FatRate.objects.all()
    farmers = Farmer.objects.all()
    if request.method == "POST":
        milk.fat = request.POST.get('fat') 
        # milk.rate = request.POST.get('rate')
        milk.qty = request.POST.get('qty')
        milk.date = request.POST.get('date')
        milk.emp_id =  Employee.objects.get(pk=request.POST['emp_id'])
        # milk.fatrate_id =  FatRate.objects.get(pk=request.POST['fatrate_id'])
        milk.farmer_id =  Farmer.objects.get(pk=request.POST['farmer_id'])
        milk.save()
        return redirect(reverse_lazy('dashboard:milk-list'))
    return render(request,'dashboard/milk/update_Form.html',
                  {'employees':employees,
                   'milk':milk,
                #    'fatrates':fatrates,
                   'farmers': farmers,
                   })

@login_required(login_url= '/dashboard/accounts/login')
def milkDeleteView(request, pk):
    milk = Milk.objects.get(pk=pk)
    milk.delete()
    return HttpResponseRedirect(reverse('dashboard:milk-list'))

#commission
@login_required(login_url= '/dashboard/accounts/login')
def commissionListView(request):
    commissions = Commission.objects.all()
    return render(request,'dashboard/commissions/list.html', {'commissions':commissions})
    
@login_required(login_url= '/dashboard/accounts/login')
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
    
@login_required(login_url= '/dashboard/accounts/login')
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

@login_required(login_url= '/dashboard/accounts/login')
def commissionDeleteView(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission.delete()
    return HttpResponseRedirect(reverse('dashboard:commissions-list'))

#Payment
@login_required(login_url= '/dashboard/accounts/login')
def paymentListView(request):
    payments = Payment.objects.all()
    return render(request,'dashboard/payments/list.html',
                  {'payments':payments})
    
@login_required(login_url= '/dashboard/accounts/login')
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


@login_required(login_url= '/dashboard/accounts/login')
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

@login_required(login_url= '/dashboard/accounts/login')
def paymentDeleteView(request, pk):
    payment = Payment.objects.get(pk=pk)
    payment.delete()
    return HttpResponseRedirect(reverse('dashboard:payments-list'))