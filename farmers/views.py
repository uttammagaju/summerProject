from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime
from user.models import *
from dashboard.models import Payment,Milk
from django.contrib import messages


# Create your views here.
@login_required(login_url="/dashboard/accounts/farmerlogin")
def farmerHomeView(request):
    current_time = datetime.datetime.now().time()
    morning_start_time = datetime.time(6,0)
    afternoon_start_time = datetime.time(12,0)
    evening_start_time = datetime.time(18,0)
    
    if morning_start_time <= current_time < afternoon_start_time:
        message = "Good Morning, "
    elif afternoon_start_time <= current_time < evening_start_time:
        message = "Good Afternoon, "
    else:
        message = "Good Evening, "

    return render(request, "farmers/index.html",{'message':message})


@login_required(login_url="/dashboard/accounts/farmerlogin")
def paymentDue(request):
    payments =  Payment.objects.filter(farmer_id=request.session.get("farmer_id"),status='unpaid').order_by('-payment_date')
    return render( request, "farmers/payment/due.html",{"payments": payments})

@login_required(login_url="/dashboard/accounts/farmerlogin")
def paymentPaid(request):
    payments =  Payment.objects.filter(farmer_id=request.session.get("farmer_id"),status='paid').order_by('-payment_date')
    return render( request, "farmers/payment/paid.html",{"payments": payments})

@login_required(login_url="/dashboard/accounts/farmerlogin")
def milkReport(request):
    if request.method=="POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        farmer_id = request.session.get("farmer_id")
        milk_datas = Milk.objects.filter(farmer_id=farmer_id, date__range=[start_date, end_date]).order_by('-date')
        print(start_date)
        return render(request, "farmers/milk/report.html",{'datas':milk_datas})
    else:
        display_datas= Milk.objects.filter(farmer_id=request.session.get("farmer_id")).order_by('-date')
        return render(request, "farmers/milk/report.html",{'datas':display_datas})

@login_required(login_url="/dashboard/accounts/farmerlogin")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        print(request.session.get("farmer_id"))
        try:
            errors = {}
            password_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            if not new_password:
                errors["new_password"] = "password field is required."
            elif not re.match(password_pattern, new_password):
                errors[
                    "new_password"
                ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

            if not confirm_password:
                errors["confirm_password"] = "password field is required."
            elif not re.match(password_pattern, confirm_password):
                errors[
                    "confirm_password"
                ] = "Invalid password format. It must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, and one digit."

            if errors:
                return render(
                    request,"farmers/change_password.html",
                    {
                        "errors": errors,
                        "current_password":current_password,
                        "new_password":new_password,
                        "confirm_password":confirm_password
                    }
                )

            else:
                u = User.objects.get(id=request.session.get("farmer_id")) 
                
                if u.check_password(current_password) and confirm_password == new_password:
                    u.set_password(new_password)
                    u.save()
                    messages.success(request, 'Password changed successfully!')
                    return render(request, "farmers/change_password.html")
                elif confirm_password!= new_password:
                    messages.error(request, 'confirm password and new password is not same')
                    return render(request, "farmers/change_password.html")
                else:
                    messages.error(request, 'Incorrect current password!')
                    return render(request, "farmers/change_password.html")
                
        except:
            pass
    return render(request, "farmers/change_password.html")
 