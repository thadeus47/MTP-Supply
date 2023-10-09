from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('login/', views.loginsupplier, name="login"),
    path('create/', views.createsupplier, name="create"),
    path('supplierdetails/', views.supplierdetails, name="supplierdetails"),
]