from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),

    #Employee
    path('employees/create',views.employeeCreateView, name = 'employees-create'),
]