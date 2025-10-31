from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Updated add endpoint with API support
    path('add/', views.add_food_log_with_api, name='add_food_log'),
    
    path('edit/<int:pk>/', views.edit_food_log, name='edit_food_log'),
    path('delete/<int:pk>/', views.delete_food_log, name='delete_food_log'),
]