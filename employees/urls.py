from django.urls import path, include

from . import views


app_name = "employees"

urlpatterns = [
    path("", views.employeeHomeView, name="home"),
    path("milk/create", views.milkCreateView, name="milk-create"),
    path("milk", views.milkListView, name="milk-list"),
    # Commission
    path("commission/due", views.commissionDue, name="commissions-due"),
    path('commission/get', views.commissionGet, name="commissions-get"),
    # payment
    path("payment/due", views.paymentDue, name = "payment-due"),
    path("payment/paid", views.paymentPaid, name = "payment-paid"),
    #change password 
    path("change_password", views.change_password, name="change_password"),



]

