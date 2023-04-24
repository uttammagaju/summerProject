from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    #Admin
    path('admins',views.AdminListView.as_view(), name = 'admins-list'),
    path('admins/create',views.adminCreateView, name ='admins-create'),
    #Employee
    path('employees',views.EmployeeListView.as_view(), name = 'employees-list'),
    path('employees/create',views.employeeCreateView, name = 'employees-create'),
    # path('employees/update/<int:pk>',views.employeeUpdate, name = 'update'),
    path('employees/<int:pk>/update',views.employeeUpdateView, name = 'employees-update'),
    path('employees/<int:pk>/delete',views.employeeDeleteView, name='employees-delete'),

]