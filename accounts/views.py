from django.shortcuts import render,redirect
from dashboard.models import *
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse_lazy
# Create your views here.
def loginView(request):
    if request.method == "POST":
        email= request.POST['email']
        password= request.POST['password']
        admin_email=Admin.objects.get(email=email)
        admin_password= Admin.objects.get(admin_pwd=password)
        error = 'Email or password didn\'t match.'
        
        user = authenticate(request, email=admin_email.email, password=admin_password.admin_pwd)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('dashboard:home'))
        else:
            return render(request,'accounts/login.html',{'error':error})
    else:
        return render(request,'accounts/login.html')

def logoutView(request):
    logout(request)
    return redirect(reverse_lazy('accounts:login'))