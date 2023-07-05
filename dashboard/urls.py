from django.urls import path, include
from . import views


app_name = "dashboard"

urlpatterns = [
    path("", views.dashboardHomeView, name="home"),
    # Employee
    path("employees", views.employeeListView, name="employees-list"),
    path("employees/create", views.employeeCreateView, name="employees-create"),
    path(
        "employees/<int:pk>/update", views.employeeUpdateView, name="employees-update"
    ),
    path(
        "employees/<int:pk>/delete", views.employeeDeleteView, name="employees-delete"
    ),
    # Farmer
    path("farmers", views.farmerListView, name="farmers-list"),
    path("farmers/create", views.farmerCreateView, name="farmers-create"),
    path("farmers/<int:pk>/update", views.farmerUpdateView, name="farmers-update"),
    path("farmers/<int:pk>/delete", views.farmerDeleteView, name="farmers-delete"),
    # #FatRate
    # path('fatrates',views.FatRateListView.as_view(), name = 'fatrates-list'),
    # path('fatrates/create',views.fatrateCreateView, name = 'fatrates-create'),
    # path('fatrates/<int:pk>/update',views.fatrateUpdateView, name = 'fatrates-update'),
    # path('fatrates/<int:pk>/delete',views.fatrateDeleteView, name='fatrates-delete'),
    # Milk
    path("milk", views.milkListView, name="milk-list"),
    # path('milk/create',views.milkCreateView, name = 'milk-create'),
    path("milk/<int:pk>/update", views.milkUpdateView, name="milk-update"),
    path("milk/<int:pk>/delete", views.milkDeleteView, name="milk-delete"),
    # Commission
    path("commissions/paid", views.commissionPaidListView, name="commissions-paid"),
    path(
        "commissions/unpaid", views.commissionUnpaidListView, name="commissions-unpaid"
    ),
    path("commissions/<int:pk>/paid", views.commissionPaid, name="commissions-paid"),
    # path('commissions/create',views.commissionCreateView, name = 'commissions-create'),
    path(
        "commissions/<int:pk>/update",
        views.commissionUpdateView,
        name="commissions-update",
    ),
    path(
        "commissions/<int:pk>/delete",
        views.commissionDeleteView,
        name="commissions-delete",
    ),
    # Payments
    path("payments/paid", views.paidListView, name="payments-paid"),
    path("payments/unpaid", views.unpaidListView, name="payments-unpaid"),
    path("payments/create", views.paymentCreateView, name="payments-create"),
    path("payments/<int:pk>/update", views.paymentUpdateView, name="payments-update"),
    path("payments/<int:pk>/delete", views.paymentDeleteView, name="payments-delete"),
    path("payments/<int:pk>/paid", views.paymentPaid, name="payments-paid"),
    path(
        "chart/filter-options/", views.get_filter_options, name="chart-filter-options"
    ),
    path("chart/milks/<int:year>/", views.get_milks_chart, name="chart-sales"),
]
