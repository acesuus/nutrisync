from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import date, timedelta  
from .models import FoodLog
from .forms import FoodLogForm
from .services import CalorieNinjasService
import json



def home(request):
    """    Home page showing:   
     - Form to add new food log    
     - Today's food logs    """   
    today = timezone.now().date()
    # Get today's food logs    
    todays_logs = FoodLog.objects.filter(date=today)
    # Initialize empty form    
    form = FoodLogForm(initial={'date': today})
    # Count logs by meal type for today    
    meal_counts = {
        'breakfast': todays_logs.filter(meal_type='breakfast').count(),
        'lunch': todays_logs.filter(meal_type='lunch').count(),
        'dinner': todays_logs.filter(meal_type='dinner').count(),
        'snack': todays_logs.filter(meal_type='snack').count(),
    }
    context = {
        'form': form,
        'todays_logs': todays_logs,
        'today': today,
        'total_logs_today': todays_logs.count(),
        'meal_counts': meal_counts,
    }
    return render(request, 'tracker/home.html', context)
    
    
def add_food_log_with_api(request):
    """
    Handle food log creation with optional API parsing
    """
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        
        # Check if natural query was provided
        natural_query = request.POST.get('natural_query', '').strip()
        
        if natural_query:
            # Use API to parse natural language
            api_service = CalorieNinjasService()
            api_response = api_service.parse_food_query(natural_query)
            
            if api_response.get('success'):
                # Format data for FoodLog
                formatted_data = api_service.format_for_food_log(
                    natural_query, 
                    api_response
                )
                
                # Pre-fill form with API data
                form.data = form.data.copy()  # Make mutable
                form.data['food_name'] = formatted_data['food_name']
                form.data['description'] = formatted_data['description']
                form.data['calories'] = formatted_data['calories']
                
                messages.success(
                    request,
                    f"✨ AI parsed your meal! Found: {formatted_data['food_name']}"
                )
            else:
                messages.warning(
                    request,
                    f"⚠️ Could not parse with AI: {api_response.get('message')}. "
                    "Please fill manually."
                )
        
        if form.is_valid():
            food_log = form.save()
            messages.success(
                request,
                f'✅ {food_log.food_name} logged successfully!'
            )
            return redirect('tracker:home')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    
    # GET request or form errors
    return redirect('tracker:home')

