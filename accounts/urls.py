from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("login", views.LoginViews.as_view(), name="login"),
    path("logout", views.LogoutViews.as_view(), name="logout"),
    path("employeelogin", views.EmployeeLoginViews.as_view(), name="employee-login"),
    path("employeelogout", views.EmployeeLogoutViews.as_view(), name="employee-logout"),
]
