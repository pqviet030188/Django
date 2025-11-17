from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    #path("", views.BillViewSet.as_view(), name="bill-list"),
    path('', views.get_bills),
    path('<int:id>/', views.get_bill),
    path('<int:bill_id>/instalments', views.get_instalments),
    path('<int:bill_id>/all-instalments', views.get_all_bill_instalments),
]
