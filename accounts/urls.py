from django.urls import path
from . import views




app_name = 'accounts'

urlpatterns = [
   path('login', views.LoginViews.as_view(), name = 'login'),
   path('logout', views.LogoutViews.as_view(), name = 'logout'),
   path('employeelogin', views.employeeLogin, name = 'employee-login'),
   path('employeelogout', views.employeeLogout, name='employee-logout')

]