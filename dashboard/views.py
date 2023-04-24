from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView
from .forms import *
from . models import *

# Create your views here.
class DashboardHomeView(TemplateView):
    template_name = "dashboard/index.html"


#Admin
class AdminListView(ListView):
    template_name = 'dashboard/admins/list.html'
    model = Admin


def adminCreateView(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        admin_pwd = request.POST.get('admin_pwd')
        data = Admin(full_name = full_name, username = username, 
                     email = email, admin_pwd = admin_pwd)
        data.save()
        return redirect(reverse_lazy('dashboard:admins-list'))
    else: 
         return render(request, "dashboard/admins/form.html")



#Employee
class EmployeeListView(ListView):
    template_name = 'dashboard/employees/list.html'
    model = Employee


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
        admin = Admin.objects.get(id=admin_id)
        Employee.objects.create(emp_email = emp_email, emp_pwd = emp_pwd ,emp_name= emp_name, 
                        emp_contact = emp_contact, salary = salary, reg_date = reg_date,
                        admin_id = admin)
        return redirect(reverse_lazy('dashboard:employees-list'))
    else:
        return render(request, "dashboard/employees/form.html",
                  {
                    'admins':Admin.objects.all(),
                  }
                  )

# def employeeUpdateView(request,pk):
#     employee_update = Employee.objects.get(pk=pk)
#     if request.method == "POST":
#         emp_email = request.POST.get('emp_email') 
#         emp_pwd = request.POST.get('emp_pwd')
#         emp_name = request.POST.get('emp_name')
#         emp_contact = request.POST.get('emp_contact')
#         salary = request.POST.get('salary')
#         reg_date= request.POST.get('reg_date')
#         admin_id = request.POST.get('admin_id')
#         admin = Admin.objects.get(id=admin_id)
#         Employee.objects.update(emp_email = emp_email, emp_pwd = emp_pwd ,emp_name= emp_name, 
#                         emp_contact = emp_contact, salary = salary, reg_date = reg_date,
#                         admin_id = admin)
#         return redirect(reverse_lazy('dashboard:employees-list'))
#     else:
#         return render(request, "dashboard/employees/update_Form.html",
#                   {
#                     'admins':Admin.objects.all(),
#                   }
#                   )

def employeeUpdateView(request, pk):
    employee = Employee.objects.get(pk=pk)
    template = loader.get_template('dashboard/employees/update_Form.html')
    context ={'employee':employee,
              'admins':Admin.objects.all(),
              }
    return HttpResponse(template.render(context, request))

def employeeDeleteView(request, pk):
    employee = Employee.objects.get(pk=pk)
    employee.delete()
    return HttpResponseRedirect(reverse('dashboard:employees-list'))