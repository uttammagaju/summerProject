from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

from dashboard.models import Payment

# Create your views here.
@login_required(login_url="/dashboard/accounts/farmerlogin")
def farmerHomeView(request):
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

    return render(request, "farmers/index.html",{'message':message})

@login_required(login_url="/dashboard/accounts/farmerlogin")
def paymentDue(request):
    payments =  Payment.objects.filter(farmer_id=request.session.get("farmer_id"),status='unpaid').order_by('-payment_date')
    return render( request, "farmers/payment/due.html",{"payments": payments})

@login_required(login_url="/dashboard/accounts/farmerlogin")
def paymentPaid(request):
    payments =  Payment.objects.filter(farmer_id=request.session.get("farmer_id"),status='paid').order_by('-payment_date')
    return render( request, "farmers/payment/paid.html",{"payments": payments})