from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta
import re, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.views import View
from .forms import *
from .models import *
from user.models import *
import requests
from django.db.models.functions import ExtractYear, ExtractMonth
from utils.charts import months, colorPrimary, get_year_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

User = get_user_model()
# request.session['admin_id'] = User.id
# Create your views here.

   
@login_required(login_url="/dashboard/accounts/login")
def dashboardHomeView(request):
    current_time = datetime.datetime.now().time()
    morning_start_time = datetime.time(6,0)
    afternoon_start_time = datetime.time(12,0)
    evening_start_time = datetime.time(18,0)
    print(current_time)
    if morning_start_time <= current_time < afternoon_start_time:
        message = "Good Morning, "
    elif afternoon_start_time <= current_time < evening_start_time:
        message = "Good Afternoon, "
    else:
        message = "Good Evening, "
    # count employee
    employee_count = EmployeeProfile.objects.filter(is_active=True).count()
    #count Farmer
    farmer_count = FarmerProfile.objects.filter(is_active=True).count()
    # calculate the total milk collected today
    total_milk_collected = Milk.objects.filter(date=date.today()).aggregate(
        total_qty=models.Sum("qty"))["total_qty"]
    # calculate the total milk collected today
    total_amount = Payment.objects.filter(payment_date=date.today(),status='unpaid').aggregate(
        total_amt=models.Sum("amt"))["total_amt"]
    
    return render(
        request,
        "dashboard/index.html",
        {
            "employee_count": employee_count,
            "total_milk_collected": total_milk_collected,
            'total_amount': total_amount,
            'farmer_count': farmer_count,
            'message': message
        }
    )


@login_required(login_url="/dashboard/accounts/login")
def employeeActiveView(request):
    employees = EmployeeProfile.objects.filter(is_active=True)
    return render(request, "dashboard/employees/active.html", {"employees": employees})

@login_required(login_url="/dashboard/accounts/login")
def employeeInactiveView(request):
    employees = EmployeeProfile.objects.filter(is_active=False)
    return render(request, "dashboard/employees/inactive.html", {"employees": employees})

@login_required(login_url="/dashboard/accounts/login")
def employeeCreateView(request):
    # request.session['admin_id']=User.id
    n = ""
    if request.method == "POST":
        emp_email = request.POST.get("emp_email")
        emp_pwd = request.POST.get("emp_pwd")
        emp_name = request.POST.get("emp_name")
        emp_contact = request.POST.get("emp_contact")
        reg_date = request.POST.get("reg_date")

        errors = {}
        # perform Validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not emp_email:
            errors["emp_email"] = "email field is requied."
        elif not re.match(email_pattern, emp_email):
            errors["emp_email"] = "email is not valid."
        elif EmployeeProfile.objects.filter(emp_email=emp_email).exists():
            errors["emp_email"] = "email is already taken."

        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if not emp_pwd:
            errors["emp_pwd"] = "password field is required."
        elif not re.match(password_pattern, emp_pwd):
            errors[
                "emp_pwd"
            ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

        name_pattern = r"^[A-Za-z\s]+$"
        if not emp_name:
            errors["emp_name"] = "name field is required."
        elif not re.match(name_pattern, emp_name):
            errors["emp_name"] = "Invalid name"
        elif EmployeeProfile.objects.filter(emp_name=emp_name).exists() or User.objects.filter(username = emp_name):
            errors["emp_name"] = "name is already taken."

        contact_pattern = r"^98\d{8}$"
        if not emp_contact:
            errors["emp_contact"] = "contact field is required."
        elif not re.match(contact_pattern, emp_contact):
            errors[
                "emp_contact"
            ] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'


        # reg_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not reg_date:
            errors["reg_date"] = "date filed is required."
        else:
            try:
                r_date = date.fromisoformat(reg_date)
                if r_date > date.today():
                    errors["reg_date"] = "Selected date cannot be in future."
            except ValueError:
                errors["reg_date"] = "Invalid date format."

        if errors:
            return render(
                request,
                "dashboard/employees/form.html",
                {
                    "errors": errors,
                    "emp_email": emp_email,
                    "emp_name": emp_name,
                    "emp_pwd": emp_pwd,
                    "emp_name": emp_name,
                    "emp_contact": emp_contact,
                    "reg_date": reg_date,
                },
            )

        else:
            employee = Employee.objects.create_user(
                username=emp_name, email=emp_email, password=emp_pwd
            )

            emp_profile = EmployeeProfile(
                user=employee,
                emp_email=emp_email,
                emp_pwd=emp_pwd,
                emp_name=emp_name,
                emp_contact=emp_contact,
                reg_date=reg_date,
                admin_id=User.objects.get(id=request.session.get("admin_id")),
            )
            EmployeeProfile.salary = 15000
            emp_profile.save()
        return redirect(reverse_lazy("dashboard:employees-list"))
    else:
        return render(
            request,
            "dashboard/employees/form.html",
            {
                "admins": User.objects.all(),
            },
        )


@login_required(login_url="/dashboard/accounts/login")
def employeeUpdateView(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    user = employee.user
    admins = User.objects.filter(is_active=True, role= 'ADMIN')
    if request.method == "POST":
        emp_email = request.POST.get("emp_email")
        emp_pwd = request.POST.get("emp_pwd")
        emp_name = request.POST.get("emp_name")
        emp_contact = request.POST.get("emp_contact")
        reg_date = request.POST.get("reg_date")
        # admin_id = User.objects.get(pk=request.POST["admin_id"])
        #validation 

        errors = {}
        # perform Validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not emp_email:
            errors["emp_email"] = "email field is requied."
        elif not re.match(email_pattern, emp_email):
            errors["emp_email"] = "email is not valid."
       

        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if not emp_pwd:
            errors["emp_pwd"] = "password field is required."
        elif not re.match(password_pattern, emp_pwd):
            errors[
                "emp_pwd"
            ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

        name_pattern = r"^[A-Za-z\s]+$"
        if not emp_name:
            errors["emp_name"] = "name field is required."
        elif not re.match(name_pattern, emp_name):
            errors["emp_name"] = "Invalid name"

        contact_pattern = r"^98\d{8}$"
        if not emp_contact:
            errors["emp_contact"] = "contact field is required."
        elif not re.match(contact_pattern, emp_contact):
            errors[
                "emp_contact"
            ] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'


        # reg_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not reg_date:
            errors["reg_date"] = "date filed is required."
        else:
            try:
                r_date = date.fromisoformat(reg_date)
                if r_date > date.today():
                    errors["reg_date"] = "Selected date cannot be in future."
            except ValueError:
                errors["reg_date"] = "Invalid date format."
        
        if errors:
            return render(
                request,
                "dashboard/employees/update_Form.html",
                {
                    "errors": errors,
                    "emp_email": emp_email,
                    "emp_name": emp_name,
                    "emp_pwd": emp_pwd,
                    "emp_name": emp_name,
                    "emp_contact": emp_contact,
                    "reg_date": reg_date,
                },
            )
        
        else:
            # Update the EmployeeProfile
            employee.emp_email = emp_email
            employee.emp_pwd = emp_pwd
            employee.emp_name = emp_name
            employee.emp_contact = emp_contact
            # employee.admin_id = admin_id
            employee.reg_date = reg_date
            employee.save()

            if user:
                user.email = emp_email
                user.username = emp_name
                user.save()

            return redirect(reverse_lazy("dashboard:employees-list"))
    return render(
        request,
        "dashboard/employees/update_Form.html",
        {
            "employee": employee,
            "reg_date": employee.reg_date.isoformat(),
            "admins": admins,
        },
    )


def update_employee_salaries(request):
    employees = EmployeeProfile.objects.all()

    for employee in employees:
        today = date.today()
        years_worked = today.year -employee.reg_date.year

        if years_worked >= 2:
            employee.salary *= 1.1 #increase salary by 10%
        if years_worked >= 4:
            employee.salary *= 1.15 #increase salary by 15%
        
        employee.save()

    return redirect ('dashboard:employee_list')


@login_required(login_url="/dashboard/accounts/login")
def employeeDeleteView(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == "POST":
        employee.is_active = False
        employee.save()

        # Set is_active to False in the User model as well
        user = employee.user
        if user:
            user.is_active = False
            user.save()

    return HttpResponseRedirect(reverse("dashboard:employees-list"))


@login_required(login_url="/dashboard/accounts/login")
def farmerActiveView(request):
    farmers = FarmerProfile.objects.filter(is_active=True)
    return render(request, "dashboard/farmers/active.html", {"farmers": farmers})

@login_required(login_url="/dashboard/accounts/login")
def farmerInactiveView(request):
    farmers = FarmerProfile.objects.filter(is_active=False)
    return render(request, "dashboard/farmers/inactive.html", {"farmers": farmers})

@login_required(login_url="/dashboard/accounts/login")
def farmerCreateView(request):
    if request.method == "POST":
        farmer_name = request.POST.get("farmer_name")
        farmer_pwd = request.POST.get("farmer_pwd")
        farmer_email = request.POST.get("farmer_email")
        farmer_address = request.POST.get("farmer_address")
        farmer_contact = request.POST.get("farmer_contact")

        errors = {}
        # perform Validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not farmer_email:
            errors["farmer_email"] = "email field is requied."
        elif not re.match(email_pattern, farmer_email):
            errors["farmer_email"] = "email is not valid."
        elif FarmerProfile.objects.filter(farmer_email=farmer_email).exists():
            errors["farmer_email"] = "email is already taken."

        password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if not farmer_pwd:
            errors["farmer_pwd"] = "email field is required."
        elif not re.match(password_pattern, farmer_pwd):
            errors[
                "farmer_pwd"
            ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

        name_pattern = r"^[A-Za-z\s]+$"
        if not farmer_name:
            errors["farmer_name"] = "name field is required."
        elif not re.match(name_pattern, farmer_name):
            errors["farmer_name"] = "Invalid name"

        contact_pattern = r"^98\d{8}$"
        if not farmer_contact:
            errors["farmer_contact"] = "contact field is required."
        elif not re.match(contact_pattern, farmer_contact):
            errors[
                "farmer_contact"
            ] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'

        address_pattern = r"^[A-Za-z\s]+$"
        if not farmer_address:
            errors["farmer_address"] = "address field is required."
        elif len(farmer_address) < 5:
            errors["farmer_address"] = "Address must contain 5 letter"
        elif not re.match(address_pattern, farmer_address):
            errors["farmer_address"] = "Invalid Address"

        if errors:
            return render(
                request,
                "dashboard/farmers/form.html",
                {
                    "errors": errors,
                    "farmer_email": farmer_email,
                    "farmer_pwd": farmer_pwd,
                    "farmer_name": farmer_name,
                    "farmer_contact": farmer_contact,
                    "farmer_address": farmer_address,
                },
            )

        else:
            farmer = Farmer.objects.create_user(
                username=farmer_name, email=farmer_email, password=farmer_pwd
            )

            farmer_profile = FarmerProfile(
                user=farmer,
                farmer_name=farmer_name,
                farmer_pwd=farmer_pwd,
                farmer_email=farmer_email,
                farmer_address=farmer_address,
                farmer_contact=farmer_contact,
                admin_id=User.objects.get(id=request.session.get("admin_id")),
            )
            farmer_profile.save()
        return redirect(reverse_lazy("dashboard:farmers-list"))
    else:
        return render(
            request,
            "dashboard/farmers/form.html",
            {
                "admins": User.objects.all(),
            },
        )


@login_required(login_url="/dashboard/accounts/login")
def farmerUpdateView(request, pk):
    farmer = get_object_or_404(FarmerProfile, pk=pk)
    user = farmer.user
    admins = User.objects.filter(is_active=True,role=User.Role.ADMIN)
    if request.method == "POST":
        farmer_name = request.POST.get("farmer_name")
        farmer_email = request.POST.get("farmer_email")
        farmer_pwd = request.POST.get("farmer_pwd")
        farmer_contact = request.POST.get("farmer_contact")
        farmer_address = request.POST.get("farmer_address")
        admin_id = User.objects.get(pk=request.POST["admin_id"],is_active=True,role=User.Role.ADMIN)
        # update
        farmer.farmer_email = farmer_email
        farmer.farmer_pwd = farmer_pwd
        farmer.farmer_name = farmer_name
        farmer.farmer_contact = farmer_contact
        farmer.farmer_address = farmer_address
        farmer.admin_id = admin_id
        farmer.save()

        if user:
            user.email = request.POST.get("farmer_email")
            user.username = request.POST.get("farmer_name")
            user.save()
            return redirect(reverse_lazy("dashboard:farmers-list"))
    return render(
        request,
        "dashboard/farmers/update_Form.html",
        {"farmer": farmer, "admins": admins},
    )


@login_required(login_url="/dashboard/accounts/login")
def farmerDeleteView(request, pk):
    farmer = get_object_or_404(FarmerProfile, pk=pk)
    if request.method == "POST":
        farmer.is_active = False
        farmer.save()

        # Set is_active to False in the User model as well
        user = farmer.user
        if user:
            user.is_active = False
            user.save()

    return HttpResponseRedirect(reverse("dashboard:farmers-list"))


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


# Milk
@login_required(login_url="/dashboard/accounts/login")
def milkListView(request):
    milks = Milk.objects.all()
    return render(request, "dashboard/milk/list.html", {"milks": milks})


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


@login_required(login_url="/dashboard/accounts/login")
def milkUpdateView(request, pk):
    milk = Milk.objects.get(pk=pk)
    employees = EmployeeProfile.objects.filter(is_active=True)
    # fatrates = FatRate.objects.all()
    farmers = FarmerProfile.objects.filter(is_active=True)
    if request.method == "POST":
        fat = request.POST.get("fat")
        qty = request.POST.get("qty")
        date_str = request.POST.get("date")
        farmer_id = request.POST.get("farmer_id")
        emp_id = request.POST.get("emp_id")

        fatrate = ""
        errors = {}
        # perform validation
        
        if not fat:
            errors["fat"] = "Fat field is required."
        elif float(fat) < 1:
            errors["fat"] = "Fat should be negative."
        elif float(fat) > 15:
            errors["fat"] = "Fat should be less than 15."

        if not qty:
            errors["qty"] = "Quantity field is required."
        elif float(qty) < 1:
            errors["qty"] = "Quantity field must be greater than 1 or positive"
        elif float(qty) >= 1 and float(qty) <= 20:
            fatrate = 14.0
        elif float(qty) > 20 and float(qty) <= 50:
            fatrate = 15.0
        elif float(qty) > 50 and float(qty) <= 150:
            fatrate = 16.0
        elif float(qty) > 150:
            fatrate = 18.0

        if not date_str:
            errors["date"] = "Date field is required"
        else:
            try:
                milk_date = date.fromisoformat(date_str)
                min_allowed_date = date.today() - timedelta(days=2)
                if milk_date > date.today():
                    errors["date"] = "Selected date cannot be in future."
                # elif milk_date < min_allowed_date:
                #     errors["date"] = "entry date cannot be more than 2 day old."
            except ValueError:
                errors["date"] = "Invalid date format."

        if not emp_id:
            errors['emp_id'] = 'Selected the employee'

        if not farmer_id:
            errors["farmer_id"] = "Selected the farmer"

        if errors:
            return render(
                request,
                "employees/milk/form.html",
                {
                    "errors": errors,
                    "fat": fat,
                    "qty": qty,
                    "date": date_str,
                    "emp_id": emp_id,
                    "farmer_id": farmer_id,
                },
            )

        else:
            emp = EmployeeProfile.objects.get(id=emp_id)
            amt = float(fat) * float(qty) * float(fatrate)


            milk.fat = fat
            milk.qty = qty
            milk.date = date_str
            milk.emp_id = EmployeeProfile.objects.get(pk=emp_id, is_active=True)
            milk.farmer_id = FarmerProfile.objects.get(pk=farmer_id,is_active=True)
            milk.save()

            if Commission.objects.filter(
                emp_id=emp, commission_pay_date=date_str).exists():
                total_quantity = Milk.objects.filter(
                    emp_id=emp, date=date_str
                ).aggregate(total_qty=models.Sum("qty"))["total_qty"]
                if total_quantity <= 500:
                    commission_rate = 0.1
                    Commission.objects.filter(emp_id=emp,commission_pay_date=date_str).update(
                        commission_amt=total_quantity * commission_rate
                    )

                elif total_quantity > 500:
                    commission_rate = 0.2
                    Commission.objects.filter(emp_id=emp,commission_pay_date=date_str).update(
                        commission_amt=total_quantity * commission_rate
                    )

            Payment.objects.filter(emp_id=emp,farmer_id=farmer_id).update(amt=amt)
            return redirect(reverse_lazy("dashboard:milk-list"))
    else:
        return render(
            request,
            "dashboard/milk/update_Form.html",
            {
                "employees": employees,
                "milk": milk,
                "farmers": farmers,
            },
        )


@login_required(login_url="/dashboard/accounts/login")
def milkDeleteView(request, pk):
    milk = Milk.objects.get(pk=pk)
    milk.delete()
    return HttpResponseRedirect(reverse("dashboard:milk-list"))


# commission
@login_required(login_url="/dashboard/accounts/login")
def commissionPaidListView(request):
    commissions = Commission.objects.filter(status='paid').order_by('-commission_pay_date')
    return render(
        request, "dashboard/commissions/paid.html", {"commissions": commissions}
    )

@login_required(login_url="/dashboard/accounts/login")
def commissionUnpaidListView(request):
    commissions = Commission.objects.filter(status='unpaid').order_by('-commission_pay_date')
    return render(
        request, "dashboard/commissions/unpaid.html", {"commissions": commissions}
    )


@login_required(login_url="/dashboard/accounts/login")
def commissionCreateView(request):
    n = ""
    if request.method == "POST":
        commission_amt = request.POST.get("commission_amt")
        commission_pay_date = request.POST.get("commission_pay_date")
        admin_id = request.POST.get("admin_id")
        admin = User.objects.get(id=admin_id)
        emp_id = request.POST.get("emp_id")
        emp = Employee.objects.get(id=emp_id)
        Commission.objects.create(
            commission_amt=commission_amt,
            commission_pay_date=commission_pay_date,
            emp_id=emp,
            admin_id=admin,
        )
        return redirect(reverse_lazy("dashboard:commissions-list"))
    else:
        return render(
            request,
            "dashboard/commissions/form.html",
            {"employees": Employee.objects.all(), "admins": User.objects.all()},
        )


@login_required(login_url="/dashboard/accounts/login")
def commissionUpdateView(request, pk):
    commissions = Commission.objects.get(pk=pk)
    employees = EmployeeProfile.objects.filter(is_active=True)
    admins = User.objects.filter(is_active=True,role=User.Role.ADMIN)
    if request.method == "POST":
        commissions.commission_amt = request.POST.get("Commission_amt")
        commissions.commission_pay_date = request.POST.get("commission_pay_date")
        commissions.admin_id = User.objects.get(pk=request.POST["admin_id"],is_active=True,role=User.Role.ADMIN)
        commissions.emp_id = EmployeeProfile.objects.get(pk=request.POST["emp_id"],is_active=True)
        commissions.save()
        return redirect(reverse_lazy("dashboard:commissions-list"))
    return render(
        request,
        "dashboard/commissions/update_Form.html",
        {
            "employees": employees,
            "commission": commissions,
            "admins": admins,
        },
    )


@login_required(login_url="/dashboard/accounts/login")
def commissionDeleteView(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission.delete()
    return HttpResponseRedirect(reverse("dashboard:commissions-list"))

@login_required(login_url="/dashboard/accounts/login")
def commissionPaid(request, pk):
    commission = Commission.objects.get(pk=pk)
    commission.status = 'paid'
    commission.commission_pay_date = date.today()
    commission.admin_id = User.objects.get(id=request.session.get("admin_id"))
    commission.save()
    return HttpResponseRedirect(reverse("dashboard:commissions-paid"))


# Payment
@login_required(login_url="/dashboard/accounts/login")
def paidListView(request):
    payments = Payment.objects.filter(status='paid').order_by('-payment_date')
    return render(request, "dashboard/payments/paid.html", {"payments": payments})

@login_required(login_url="/dashboard/accounts/login")
def unpaidListView(request):
    payments = Payment.objects.filter(status='unpaid').order_by('-payment_date')
    return render(request, "dashboard/payments/unpaid.html", {"payments": payments})

@login_required(login_url="/dashboard/accounts/login")
def paymentCreateView(request):
    n = ""
    if request.method == "POST":
        amt = request.POST.get("amt")
        payment_date = request.POST.get("payment_date")
        admin_id = request.POST.get("admin_id")
        admin = User.objects.get(id=admin_id)
        farmer_id = request.POST.get("farmer_id")
        farmer = FarmerProfile.objects.get(id=farmer_id)
        Payment.objects.create(
            amt=amt, payment_date=payment_date, admin_id=admin, farmer_id=farmer
        )
        return redirect(reverse_lazy("dashboard:payments-list"))
    else:
        return render(
            request,
            "dashboard/payments/form.html",
            {"farmers": FarmerProfile.objects.all(), "admins": User.objects.all()},
        )


@login_required(login_url="/dashboard/accounts/login")
def paymentUpdateView(request, pk):
    payments = Payment.objects.get(pk=pk)
    farmers = FarmerProfile.objects.all()
    admins = User.objects.all()
    if request.method == "POST":
        payments.amt = request.POST.get("amt")
        payments.payment_date = request.POST.get("payment_date")
        payments.admin_id = User.objects.get(pk=request.POST["admin_id"])
        payments.farmer_id = FarmerProfile.objects.get(pk=request.POST["farmer_id"])
        payments.save()
        return redirect(reverse_lazy("dashboard:payments-list"))
    return render(
        request,
        "dashboard/payments/update_Form.html",
        {
            "farmers": farmers,
            "payment": payments,
            "admins": admins,
        },
    )


@login_required(login_url="/dashboard/accounts/login")
def paymentDeleteView(request, pk):
    payment = Payment.objects.get(pk=pk)
    request.session['payment_id'] = pk
    payment.delete()
    return HttpResponseRedirect(reverse("dashboard:payments-list"))

@login_required(login_url="/dashboard/accounts/login")
def paymentPaidKhalti(request, pk):
    payments = Payment.objects.get(pk=pk)
    request.session['payment_id'] = pk
    print(request.session.get('payment_id'))
    farmer_name = payments.farmer_id.farmer_name
    
    return render(request, "dashboard/payments/payment.html",{"payments":payments,"farmer_name":farmer_name})
    

def get_filter_options(request):
    grouped_milk = Milk.objects.annotate(year = ExtractYear("date")).values("year").order_by("-year").distinct()
    options = [milkCreateView["year"] for milkCreateView in grouped_milk ]
    return JsonResponse({"options":options,})

def get_milks_chart(request, year):
    milks = Milk.objects.filter(date__year=year)
    grouped_milks = milks.annotate(month=ExtractMonth("date")) \
        .values("month").annotate(total=Sum(F("fat") * F("rate") * F("qty"))).values("month", "total").order_by("month")

    milks_dict = get_year_dict()  # Assuming you have a function to get a dictionary with all months

    for group in grouped_milks:
        milks_dict[months[group["month"] - 1]] = round(group["total"], 2)

    return JsonResponse({
        "title": f"Milk Sales in {year}",
        "data": {
            "labels": list(milks_dict.keys()),
            "datasets": [{
                "label": "Amount (Rs)",
                "backgroundColor": colorPrimary,  # Assuming you have defined the colorPrimary variable
                "borderColor": colorPrimary,
                "data": list(milks_dict.values()),
            }]
        },
    })

# Esewa API integrate
@csrf_exempt
def verify_payment(request):
    # data = request.POST
    # product_id = data['product_identity']
    # token = data['token']
    # amount = data['amount']

    # url = "https://khalti.com/api/v2/payment/verify/"
    # payload = {
    # "token": token,
    # "amount": amount
    # }
    # headers = {
    # "Authorization": "test_secret_key_84070ae476e84785b4a88eb7cc4ffc22"
    # }
    if request.method == 'POST':
        data = request.POST
        product_id = data.get('product_identity')
        token = data.get('token')
        amount = data.get('amount')

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "test_secret_key_84070ae476e84785b4a88eb7cc4ffc22"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            status_code = str(response.status_code)
 
            print(status_code)
            if response.status_code == 302:
                redirect_url = response.headers['Location']
                return JsonResponse({'redirect_url': redirect_url})
            
            return JsonResponse(response_data)
            # elif status_code == '200':
            #     payment = Payment.objects.get(id=request.session.get('payment_id'))
            #     print(request.session.get('admin_id'))
            #     payment.status = 'paid'
            #     payment.payment_date = date.today()
            #     payment.admin_id = User.objects.get(id=request.session.get('admin_id'))
            #     payment.save()
            #     return redirect(reverse_lazy("dashboard:payments-paid"))
            # else:
            #     return redirect(reverse_lazy("dashboard:payments-unpaid"))
          
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            return JsonResponse({'error': error_message}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url="/dashboard/accounts/login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        try:
            u = User.objects.get(id=request.session.get("admin_id")) 
            if u.check_password(current_password) and confirm_password == new_password:
                u.set_password(new_password)
                u.save()
                messages.success(request, 'Password changed successfully!')
                return render(request, "accounts/change_password.html")
            elif confirm_password!= new_password:
                messages.error(request, 'change password and new password is not same')
                return render(request, "accounts/change_password.html")
            else:
                messages.error(request, 'Incorrect current password!')
                return render(request, "accounts/change_password.html")
             
        except:
            pass
    return render(request, "dashboard/change_password.html")
 