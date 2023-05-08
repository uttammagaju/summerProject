from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    #Admin
    # path('admins',views.AdminListView.as_view(), name = 'admins-list'),
    # path('admins/create',views.adminCreateView, name ='admins-create'),
    # path('admins/<int:pk>/delete',views.AdminDeleteView.as_view(), name='admins-delete'),
    #Employee
    path('employees',views.EmployeeListView.as_view(), name = 'employees-list'),
    path('employees/create',views.employeeCreateView, name = 'employees-create'),
    path('employees/<int:pk>/update',views.employeeUpdateView, name = 'employees-update'),
    path('employees/<int:pk>/delete',views.employeeDeleteView, name='employees-delete'),

    #Farmer
    path('farmers',views.FarmerListView.as_view(), name = 'farmers-list'),
    path('farmers/create',views.farmerCreateView, name = 'farmers-create'),
    path('farmers/<int:pk>/update',views.farmerUpdateView, name = 'farmers-update'),
    path('farmers/<int:pk>/delete',views.farmerDeleteView, name='farmers-delete'),

    #FatRate
    path('fatrates',views.FatRateListView.as_view(), name = 'fatrates-list'),
    path('fatrates/create',views.fatrateCreateView, name = 'fatrates-create'),
    # path('fatrates/<int:pk>/update',views.fatrateUpdateView, name = 'fatrates-update'),
    path('fatrates/<int:pk>/delete',views.fatrateDeleteView, name='fatrates-delete'),
]