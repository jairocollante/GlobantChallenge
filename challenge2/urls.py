from django.urls import path
from . import views

urlpatterns = [
    path('employees_quarter/', views.employees_quarter),    
    path('employees_hired/', views.employees_hired),
]
