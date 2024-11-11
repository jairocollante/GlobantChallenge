from django.urls import path
from . import views

urlpatterns = [
    path('new_data/', views.new_data),    
    path('backup/', views.backup),
    path('restore/', views.restore),     
]
