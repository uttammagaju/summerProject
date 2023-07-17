from django.urls import path

from . import views


app_name = "farmers"

urlpatterns = [
    path("", views.farmerHomeView, name="home"),
    # # payment
    path("payment/due", views.paymentDue, name = "payment-due"),
    path("payment/paid", views.paymentPaid, name = "payment-paid"),
    path("milk/report",views.milkReport, name= "milk-report"),

    #change password
    path("change_password", views.change_password, name="change_password"),
]

