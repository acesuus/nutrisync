from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Food log management
    path('add/', views.add_food_log, name='add_food_log'),
    path('edit/<int:pk>/', views.edit_food_log, name='edit_food_log'),
    path('delete/<int:pk>/', views.delete_food_log, name='delete_food_log'),
    
    # User management
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]