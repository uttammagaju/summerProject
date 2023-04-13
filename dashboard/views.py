from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from . models import *

# Create your views here.
class DashboardHomeView(TemplateView):
    template_name = "dashboard/index.html"

def employeeCreateView(request):
    if request.method == "POST":
        emp_email = request.POST.get('emp_email') 
        emp_pwd = request.POST.get('emp_pwd')
        emp_name = request.POST.get('emp_name')
        emp_contact = request.POST.get('emp_contact')
        salary = request.POST.get('salary')
        reg_date= request.POST.get('reg_date')
        admin_id = request.POST.get('admin_id')
        commission_amt = request.POST.get('comission_amt')
        data = Employee(emp_email = emp_email, emp_pwd = emp_pwd ,emp_name= emp_name, 
                        emp_contact = emp_contact, salary = salary, reg_date = reg_date,
                        admin_id = admin_id, commission_amt = commission_amt)
        data.save()
    return render(request, "form.html")