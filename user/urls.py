from django.urls import path, include
from . import views

app_name = "user"

urlpatterns = [
    # path("", views.userHomeView, name="home"),
    # # Admin
    # # path('admins',views.AdminListView.as_view(), name = 'admins-list'),
    # # path('admins/create',views.adminCreateView, name ='admins-create'),
    # # path('admins/<int:pk>/delete',views.AdminDeleteView.as_view(), name='admins-delete'),
    # # Employee
    # path("employees", views.employeeListView, name="employees-list"),
    # path("employees/create", views.employeeCreateView, name="employees-create"),
    # path(
    #     "employees/<int:pk>/update", views.employeeUpdateView, name="employees-update"
    # ),
    # path(
    #     "employees/<int:pk>/delete", views.employeeDeleteView, name="employees-delete"
    # ),
    # path("farmers", views.farmerListView, name="farmers-list"),
    # path("farmers/create", views.farmerCreateView, name="farmers-create"),
]
