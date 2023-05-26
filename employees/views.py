from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from dashboard.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url= '/employees/accounts/employeelogin')   
def employeeHomeView(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('accounts:employee-login'))
    return render(request, "employees/index.html")

#milk
def milkListView(request):
    milks = Milk.objects.all()
    return render(request, "employees/milk/list.html", {'milks':milks})

# @login_required(login_url = '/employees/accounts/employeelogin')
def milkCreateView(request):
    n=''
    if request.method == "POST":
        fat = request.POST.get('fat') 
        qty = request.POST.get('qty')
        date_str = request.POST.get('date')
        # emp_id = request.POST.get('emp_id')
        # if emp_id:
        #     emp = Employee.objects.get(id=emp_id)
        # else:
        #     return HttpResponse("Please select an employee")
        farmer_id = request.POST.get('farmer_id')
        if farmer_id:
            farmer = Farmer.objects.get(id=farmer_id)
        else:
            return HttpResponse("Please select an farmer")
        
        
        fatrate=''
        errors ={}
        #perform validation
        # if emp is '':
        #     HttpResponse("please select employee")

        if not fat:
            errors['fat'] ='Fat field is required.'
        elif float(fat)<1:
            errors['fat'] ='Fat should be negative.'
        elif float(fat)>15:
            errors['fat'] ='Fat should be less than 15.'
            

        if not qty:
            errors['qty']='Quantity field is required.'
        elif float(qty)<1:
            errors['qty']='Quantity field must be greater than 1 or positive'
        elif float(qty)>=1 and float(qty)<=20:
            fatrate=14.0
        elif float(qty)>20 and float(qty)<=50:
            fatrate=15.0
        elif float(qty)>50 and float(qty)<=100:
            fatrate=16.0
        elif float(qty)>150:
            fatrate=20.0
        
        if not date_str:
            errors['date']='Date field is required'
        else:
            try: 
                milk_date = date.fromisoformat(date_str)
                min_allowed_date = date.today() - timedelta(days=2)
                if milk_date > date.today():
                    errors['date'] = 'Selected date cannot be in future.' 
                elif milk_date < min_allowed_date:
                    errors['date'] = 'entry date cannot be more than 2 day old.'
            except ValueError:
                errors['date'] = 'Invalid date format.'

        # if not emp_id:
        #     errors['emp_id'] = 'Selected the employee'

        if not farmer_id:
            errors['farmer_id']= 'Selected the farmer'

        if errors:
            return render(request,"employees/milk/form.html",{'errors': errors,'fat': fat, 'qty': qty,'date': date_str,'emp_id' : emp, 'farmer_id': farmer})
        
        else:
            emp = Employee.objects.get(id = request.session.get('employee_id'))
            # admin = User.objects.get(id=request.session.get('admin_id')) 
            # admin = 'null'
            #calculate the payment amt
            amt =float(fat) * float(qty) * float(fatrate)

            #create milk object
            Milk.objects.create(fat = fat, qty= qty, date = date_str, rate = fatrate, emp_id = emp, farmer_id = farmer)
            #calculate commission
            fill_date = date.today()

            if Commission.objects.filter(emp_id=emp ,commission_pay_date =fill_date).exists():
                total_quantity = Milk.objects.filter(emp_id=emp, date=fill_date).aggregate(total_qty=models.Sum('qty'))['total_qty']
                if total_quantity <=500:
                    commission_rate = 0.1
                    Commission.objects.filter(emp_id=emp).update(commission_amt=total_quantity*commission_rate)

                elif total_quantity > 500:
                    commission_rate = 0.2
                    Commission.objects.filter(emp_id=emp).update(commission_amt=total_quantity*commission_rate)
            
            else:
                if not  Commission.objects.filter(emp_id=emp ,commission_pay_date =fill_date).exists():
                    if float(qty) <= 500:
                        commission_rate = 0.1
                    elif float(qty) >= 1000:
                        commission_rate = 0.2
                    first_amt = float(qty) * commission_rate
                    Commission.objects.create(commission_amt = first_amt, commission_pay_date = date_str ,emp_id = emp)

           
                # pay_date = Commission.objects.get('commission_pay_date')
                # if Commission.object.filter(fill_date = pay_date):
                #     f


            #create payment object
            Payment.objects.create(amt = amt, emp_id = emp ,payment_date = date_str, farmer_id = farmer, )
            return redirect(reverse_lazy('employees:milk-list'))
    else:
        return render(request, "employees/milk/form.html",
                  {
                    'employees': Employee.objects.all(),
                    # 'fatrates' : FatRate.objects.all(),
                    'farmers'  : Farmer.objects.all()
                  }
                  )
    
#commission
def commissionDue(request):
    commissions = Commission.objects.all()
    return render(request, 'employees/commission/due.html',{'commissions':commissions})