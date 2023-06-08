# from datetime import date
# import re
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse, reverse_lazy
# from django.contrib.auth.decorators import login_required


# from user.models import EmployeeProfile, Farmer, User, Employee, FarmerProfile


# # Create your views here.
# @login_required(login_url="/user/accounts/login")
# def dashboardHomeView(request):
#     # count employee
#     employee_count = EmployeeProfile.objects.count()
#     # callculate the total milk collected today
#     # total_milk_collected = Milk.objects.filter(date = date.today()).aggregate(total_qty=models.Sum('qty'))['total_qty']
#     return render(
#         request,
#         "user/index.html",
#         {
#             "employee_count": employee_count
#             #   ,'total_milk_collected': total_milk_collected
#         },
#     )


# def employeeListView(request):
#     employees = EmployeeProfile.objects.filter(is_active=True)
#     return render(request, "user/employees/list.html", {"employees": employees})


# def employeeCreateView(request):
#     # request.session['admin_id']=User.id
#     n = ""
#     if request.method == "POST":
#         emp_email = request.POST.get("emp_email")
#         emp_pwd = request.POST.get("emp_pwd")
#         emp_name = request.POST.get("emp_name")
#         emp_contact = request.POST.get("emp_contact")
#         salary = request.POST.get("salary")
#         reg_date = request.POST.get("reg_date")


#         errors = {}
#         # perform Validation
#         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not emp_email:
#             errors["emp_email"] = "email field is requied."
#         elif not re.match(email_pattern, emp_email):
#             errors["emp_email"] = "email is not valid."
#         # elif Employee.objects.filter(emp_email=emp_email).exists():
#         #     errors['emp_email'] = 'email is already taken.'

#         password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
#         if not emp_pwd:
#             errors["emp_pwd"] = "password field is required."
#         elif not re.match(password_pattern, emp_pwd):
#             errors[
#                 "emp_pwd"
#             ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

#         name_pattern = r"^[A-Za-z\s]+$"
#         if not emp_name:
#             errors["emp_name"] = "name field is required."
#         elif not re.match(name_pattern, emp_name):
#             errors["emp_name"] = "Invalid name"

#         contact_pattern = r"^98\d{8}$"
#         if not emp_contact:
#             errors["emp_contact"] = "contact field is required."
#         elif not re.match(contact_pattern, emp_contact):
#             errors[
#                 "emp_contact"
#             ] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'

#         salary_pattern = r"^[1-9]\d*(\.\d+)?$"
#         if not salary:
#             errors["salary"] = "salary field is required."
#         elif not re.match(salary_pattern, salary):
#             errors["salary"] = "Invalid salary format. It must be a number."
#         elif float(salary) > 15000:
#             errors["salary"] = "Invalid salary. Maximum salary is 15000."

#         # reg_date_pattern = r'^\d{4}-\d{2}-\d{2}$'
#         if not reg_date:
#             errors["reg_date"] = "date filed is required."
#         else:
#             try:
#                 r_date = date.fromisoformat(reg_date)
#                 if r_date > date.today():
#                     errors["reg_date"] = "Selected date cannot be in future."
#             except ValueError:
#                 errors["reg_date"] = "Invalid date format."

#         if errors:
#             return render(
#                 request,
#                 "user/employees/form.html",
#                 {
#                     "errors": errors,
#                     "emp_email": emp_email,
#                     "emp_name": emp_name,
#                     "emp_pwd": emp_pwd,
#                     "emp_name": emp_name,
#                     "emp_contact": emp_contact,
#                     "salary": salary,
#                     "reg_date": reg_date,

#                 },
#             )

#         else:
#             employee = Employee.objects.create_user(
#                 username=emp_name, email=emp_email, password=emp_pwd
#             )

#             emp_profile = EmployeeProfile(
#                 user=employee,
#                 emp_email=emp_email,
#                 emp_pwd=emp_pwd,
#                 emp_name=emp_name,
#                 emp_contact=emp_contact,
#                 salary=salary,
#                 reg_date=reg_date,
#                 admin_id = User.objects.get(id=request.session.get('admin_id'))
#             )
#             emp_profile.save()
#         return redirect(reverse_lazy("user:employees-list"))
#     else:
#         return render(
#             request,
#             "user/employees/form.html",
#             {
#                 "admins": User.objects.all(),
#             },
#         )


# def employeeUpdateView(request, pk):
#     employee = get_object_or_404(EmployeeProfile, pk=pk)
#     user = employee.user
#     admins = User.objects.all()
#     if request.method == "POST":
#         emp_email = request.POST.get('emp_email')
#         emp_pwd = request.POST.get('emp_pwd')
#         emp_name = request.POST.get('emp_name')
#         emp_contact = request.POST.get('emp_contact')
#         salary = request.POST.get('salary')
#         reg_date = request.POST.get('reg_date')
#         admin_id = User.objects.get(pk=request.POST["admin_id"])


#         #Update the EmployeeProfile
#         employee.emp_email = emp_email
#         employee.emp_pwd = emp_pwd
#         employee.emp_name = emp_name
#         employee.emp_contact = emp_contact
#         employee.salary = salary
#         employee.admin_id = admin_id
#         employee.reg_date = reg_date
#         employee.save()

#         if user:
#             user.email = request.POST["emp_email"]
#             user.username = request.POST["emp_name"]
#             user.save()

#         return redirect(reverse_lazy("user:employees-list"))
#     return render(
#         request,
#         "user/employees/update_Form.html",
#         {"employee": employee, "reg_date": employee.reg_date.isoformat(),"admins": admins},
#     )


# def employeeDeleteView(request, pk):
#     employee = get_object_or_404(EmployeeProfile, pk=pk)
#     if request.method == "POST":
#         employee.is_active = False
#         employee.save()

#         # Set is_active to False in the User model as well
#         user = employee.user
#         if user:
#             user.is_active = False
#             user.save()

#     return HttpResponseRedirect(reverse("user:employees-list"))


# def farmerListView(request):
#     farmers = Farmer.objects.all()
#     return render(request, "user/farmers/list.html", {"farmers": farmers})


# def farmerCreateView(request):
#     if request.method == "POST":
#         farmer_name = request.POST.get("farmer_name")
#         farmer_pwd = request.POST.get("farmer_pwd")
#         farmer_email = request.POST.get("farmer_email")
#         farmer_address = request.POST.get("farmer_address")
#         farmer_contact = request.POST.get("farmer_contact")

#         errors = {}
#         # perform Validation
#         email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not farmer_email:
#             errors["farmer_email"] = "email field is requied."
#         elif not re.match(email_pattern, farmer_email):
#             errors["farmer_email"] = "email is not valid."
#         elif Farmer.objects.filter(farmer_email=farmer_email).exists():
#             errors["farmer_email"] = "email is already taken."

#         password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
#         if not farmer_pwd:
#             errors["farmer_pwd"] = "email field is required."
#         elif not re.match(password_pattern, farmer_pwd):
#             errors[
#                 "farmer_pwd"
#             ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

#         name_pattern = r"^[A-Za-z\s]+$"
#         if not farmer_name:
#             errors["farmer_name"] = "name field is required."
#         elif not re.match(name_pattern, farmer_name):
#             errors["farmer_name"] = "Invalid name"

#         contact_pattern = r"^98\d{8}$"
#         if not farmer_contact:
#             errors["farmer_contact"] = "contact field is required."
#         elif not re.match(contact_pattern, farmer_contact):
#             errors[
#                 "farmer_contact"
#             ] = 'Invalid contact number format. It must start with "98" and have a length of 10 digits.'

#         address_pattern = r"^\d+\s+([A-Za-z]+\s?)+,\s*\w+,\s*\w+\s*\d*$"
#         if not farmer_address:
#             errors["farmer_address"] = "address field is required."
#         # elif len(farmer_address) < 5:
#         #     errors["farmer_address"] = "Address must contain 5 letter"
#         elif not re.match(address_pattern, farmer_address):
#             errors["farmer_address"] = "Invalid Address"


#         if errors:
#             return render(
#                 request,
#                 "user/farmers/form.html",
#                 {
#                     "errors": errors,
#                     "farmer_email": farmer_email,
#                     "farmer_pwd": farmer_pwd,
#                     "farmer_name": farmer_name,
#                     "farmer_contact": farmer_contact,
#                     "farmer_address": farmer_address
#                 },
#             )

#         else:
#             farmer = Farmer.objects.create_user(
#                 username = farmer_name, email = farmer_email, password = farmer_pwd
#             )
#             farmer_profile = FarmerProfile(
#                 farmer_name = farmer_name,
#                 farmer_pwd = farmer_pwd,
#                 farmer_email = farmer_email,
#                 farmer_address = farmer_address,
#                 farmer_contact = farmer_contact,
#                 admin_id = User.objects.get(id=request.session.get('admin_id'))
#             )
#             farmer_profile.save()
#         return redirect(reverse_lazy("user:farmers-list"))
#     else:
#         return render(
#             request,
#             "user/farmers/form.html",
#             {
#                 "admins": User.objects.all(),
#             },
#         )

# def farmerUpdateView(request, pk):
#     farmer = get_object_or_404(FarmerProfile, pk=pk)
#     user = farmer.user
#     admins = User.objects.all()
#     if request.method == "POST":
#         farmer_name = request.POST.get("farmer_name")
#         farmer_email = request.POST.get("farmer_email")
#         farmer_pwd = request.POST.get("farmer_pwd")
#         farmer_contact = request.POST.get("farmer_contact")
#         farmer_address = request.POST.get("farmer_address")
#         admin_id  = User.objects.get(pk=request.POST["admin_id"])
#         #update
#         farmer.farmer_email = farmer_email
#         farmer.farmer_pwd = farmer_pwd
#         farmer.farmer_name = farmer_name
#         farmer.farmer_contact = farmer_contact
#         farmer.farmer_address = farmer_address
#         farmer.admin_id = admin_id
#         farmer.save()

#         if user:
#             user.email = request.POST.get("farmer_email")
#             user.username = request.POST.get("farmer_name")
#             user.save()
#             return redirect(reverse_lazy("user:farmers-list"))
#     return render(
#         request,
#         "user/farmers/update_Form.html",
#         {"farmer": farmer, "admins": admins},
#     )


# def farmerDeleteView(request, pk):
#     farmer = get_object_or_404(FarmerProfile, pk=pk)
#     if request.method == "POST":
#         farmer.is_active = False
#         farmer.save()

#         # Set is_active to False in the User model as well
#         user = farmer.user
#         if user:
#             user.is_active = False
#             user.save()

#     return HttpResponseRedirect(reverse("user:farmers-list"))
