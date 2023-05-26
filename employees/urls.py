from django.urls import path, include

from . import views


app_name = 'employees'

urlpatterns = [
    
    path('', views.employeeHomeView, name ='home'),
    path('milk/create', views.milkCreateView, name = 'milk-create'),
    path('milk', views.milkListView, name = 'milk-list'),
    #Commission
    path('commission/due',views.commissionDue, name = 'commission-due' )
]