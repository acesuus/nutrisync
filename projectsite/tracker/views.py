from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import date, timedelta  
from .models import FoodLog
from .forms import FoodLogForm
from .services import CalorieNinjasService
from .utils import calculate_statistics, prepare_chart_data
import json
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Home page - requires login"""
    """Home page showing:   
     - Form to add new food log    
     - Today's food logs"""   
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
    
    # Calculate today's nutrition totals for JavaScript
    nutrition_totals = {
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0,
        'sodium': 0,
        'sugar': 0,
        'potassium': 0,
        'cholesterol': 0,
        'saturated_fat': 0,
        'calories': 0
    }
    
    for log in todays_logs:
        if log.nutrition_data:
            nutrition_totals['protein'] += float(log.nutrition_data.get('protein_g', 0))
            nutrition_totals['carbs'] += float(log.nutrition_data.get('carbohydrates_total_g', 0))
            nutrition_totals['fat'] += float(log.nutrition_data.get('fat_total_g', 0))
            nutrition_totals['fiber'] += float(log.nutrition_data.get('fiber_g', 0))
            nutrition_totals['sodium'] += float(log.nutrition_data.get('sodium_mg', 0))
            nutrition_totals['sugar'] += float(log.nutrition_data.get('sugar_g', 0))
            nutrition_totals['potassium'] += float(log.nutrition_data.get('potassium_mg', 0))
            nutrition_totals['cholesterol'] += float(log.nutrition_data.get('cholesterol_mg', 0))
            nutrition_totals['saturated_fat'] += float(log.nutrition_data.get('saturated_fat_g', 0))
            # Prefer nutrition_data calories over model field
            nutrition_totals['calories'] += float(log.nutrition_data.get('calories', log.calories or 0))
        else:
            nutrition_totals['calories'] += float(log.calories or 0)
    
    context = {
        'form': form,
        'todays_logs': todays_logs,
        'today': today,
        'total_logs_today': todays_logs.count(),
        'meal_counts': meal_counts,
        'nutrition_totals': nutrition_totals,
    }
    return render(request, 'tracker/home.html', context)


@login_required
def add_food_log(request):
    """Add food log - requires login"""
    """Handle POST request to save new food log with AI parsing"""    
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        
        # Get natural query from form
        natural_query = request.POST.get('natural_query', '').strip()
        
        if not natural_query:
            messages.error(request, '❌ Please describe what you ate.')
            return redirect('tracker:home')
        
        if form.is_valid():
            # Use API to parse natural language
            api_service = CalorieNinjasService()
            api_response = api_service.parse_food_query(natural_query)
            
            if api_response.get('success'):
                # Format data for FoodLog
                formatted_data = api_service.format_for_food_log(
                    natural_query, 
                    api_response
                )
                
                # Create food log with API data including nutrition
                food_log = form.save(commit=False)
                food_log.food_name = formatted_data['food_name']
                food_log.description = formatted_data['description']
                food_log.calories = formatted_data['calories']
                food_log.nutrition_data = formatted_data.get('nutrition', {})
                food_log.save()
                
                messages.success(
                    request,
                    f"{food_log.food_name} logged successfully!"
                )
                return redirect('tracker:home')
            else:
                messages.error(
                    request,
                    f"{api_response.get('message', 'Unknown error')}"
                )
                return redirect('tracker:home')
        else:
            # Show error message           
            messages.error(request, '❌ Please correct the errors below.')
            # Re-display the form with errors            
            today = timezone.now().date()
            todays_logs = FoodLog.objects.filter(date=today)
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
    
    # If not POST, redirect to home    
    return redirect('tracker:home')


@login_required
def edit_food_log(request, pk):
    """Edit food log - requires login"""
    """Edit an existing food log.    
    GET: Display pre-filled form    
    POST: Update the food log"""    
    # Get the food log or return 404 if not found    
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    if request.method == 'POST':
        # Bind form with POST data and existing instance        
        form = FoodLogForm(request.POST, instance=food_log)
        if form.is_valid():
            # Preserve nutrition data when updating
            updated_log = form.save(commit=False)
            if not updated_log.nutrition_data and food_log.nutrition_data:
                updated_log.nutrition_data = food_log.nutrition_data
            updated_log.save()
            messages.success(
                request,
                f'✅ {updated_log.food_name} updated successfully!'
            )
            return redirect('tracker:home')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        # Display pre-filled form        
        form = FoodLogForm(instance=food_log)
    context = {
        'form': form,
        'food_log': food_log,
        'is_editing': True,
    }
    return render(request, 'tracker/edit_food_log.html', context)


@login_required
def delete_food_log(request, pk):
    """Delete food log - requires login"""
    """Delete a food log with confirmation.    
    GET: Show confirmation page    
    POST: Delete the food log"""    
    food_log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    if request.method == 'POST':
        food_name = food_log.food_name
        food_log.delete()
        messages.success(
            request,
            f'🗑️ {food_name} has been deleted.'
        )
        return redirect('tracker:home')
    context = {
        'food_log': food_log,
    }
    return render(request, 'tracker/delete_confirm.html', context)


@login_required
def dashboard(request):
    """Dashboard - requires login"""
    """
    Dashboard showing daily nutrition with:
    - Day-by-day navigation
    - Daily nutrient totals
    - Charts data
    """
    # Filter by current user
    food_logs = FoodLog.objects.filter(user=request.user)
    
    # Get the current date from query parameter or default to today
    date_param = request.GET.get('date')
    today = timezone.now().date()
    
    if date_param:
        try:
            from datetime import datetime
            current_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            current_date = today
    else:
        current_date = today
    
    # Calculate previous and next dates
    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)
    is_today = current_date == today
    
    # Get food logs for the current date
    food_logs = FoodLog.objects.filter(date=current_date)
    daily_meals_count = food_logs.count()
    
    # Calculate daily nutrition totals
    daily_nutrition = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0,
        'sugar': 0,
        'sodium': 0,
        'potassium': 0,
        'cholesterol': 0,
        'saturated_fat': 0,
    }
    
    for log in food_logs:
        if log.nutrition_data:
            daily_nutrition['protein'] += float(log.nutrition_data.get('protein_g', 0))
            daily_nutrition['carbs'] += float(log.nutrition_data.get('carbohydrates_total_g', 0))
            daily_nutrition['fat'] += float(log.nutrition_data.get('fat_total_g', 0))
            daily_nutrition['fiber'] += float(log.nutrition_data.get('fiber_g', 0))
            daily_nutrition['sodium'] += float(log.nutrition_data.get('sodium_mg', 0))
            daily_nutrition['sugar'] += float(log.nutrition_data.get('sugar_g', 0))
            daily_nutrition['potassium'] += float(log.nutrition_data.get('potassium_mg', 0))
            daily_nutrition['cholesterol'] += float(log.nutrition_data.get('cholesterol_mg', 0))
            daily_nutrition['saturated_fat'] += float(log.nutrition_data.get('saturated_fat_g', 0))
            daily_nutrition['calories'] += float(log.nutrition_data.get('calories', log.calories or 0))
        else:
            daily_nutrition['calories'] += float(log.calories or 0)
    
    # Prepare comprehensive chart data (last 7 days)
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Initialize chart data structures
    calories_data = []
    protein_data = []
    carbs_data = []
    fat_data = []
    
    # Calorie goal (you can make this dynamic per user later)
    calorie_goal = 2000
    
    for day in last_7_days:
        day_logs = FoodLog.objects.filter(date=day)
        
        # Calculate daily totals
        day_calories = 0
        day_protein = 0
        day_carbs = 0
        day_fat = 0
        
        for log in day_logs:
            if log.nutrition_data:
                # DEBUG: Print nutrition_data keys for today's logs
                if day == current_date:
                    print(f"DEBUG - Food: {log.food_name}")
                    print(f"DEBUG - nutrition_data keys: {list(log.nutrition_data.keys())}")
                    print(f"DEBUG - nutrition_data: {log.nutrition_data}")
                    print(f"DEBUG - carbohydrates_total_g value: {log.nutrition_data.get('carbohydrates_total_g', 'NOT FOUND')}")
                
                day_protein += float(log.nutrition_data.get('protein_g', 0))
                # Try multiple possible field names for carbohydrates
                carbs_value = (
                    log.nutrition_data.get('carbohydrates_total_g') or
                    log.nutrition_data.get('carbohydrates_g') or
                    log.nutrition_data.get('carbs') or
                    0
                )
                day_carbs += float(carbs_value)
                day_fat += float(log.nutrition_data.get('fat_total_g', 0))
                day_calories += float(log.nutrition_data.get('calories', log.calories or 0))
            else:
                day_calories += float(log.calories or 0)
        
        # Add to chart data
        calories_data.append({
            'date': day.strftime('%m/%d'),
            'calories': round(day_calories, 1)
        })
        protein_data.append({
            'date': day.strftime('%m/%d'),
            'value': round(day_protein, 1)
        })
        carbs_data.append({
            'date': day.strftime('%m/%d'),
            'value': round(day_carbs, 1)
        })
        fat_data.append({
            'date': day.strftime('%m/%d'),
            'value': round(day_fat, 1)
        })
    
    # Convert to JSON for JavaScript
    calories_chart_json = json.dumps(calories_data)
    protein_chart_json = json.dumps(protein_data)
    carbs_chart_json = json.dumps(carbs_data)
    fat_chart_json = json.dumps(fat_data)
    
    context = {
        'current_date': current_date,
        'prev_date': prev_date.strftime('%Y-%m-%d'),
        'next_date': next_date.strftime('%Y-%m-%d'),
        'is_today': is_today,
        'food_logs': food_logs,
        'daily_meals_count': daily_meals_count,
        'daily_nutrition': daily_nutrition,
        'calorie_goal': calorie_goal,
        'calories_chart_json': calories_chart_json,
        'protein_chart_json': protein_chart_json,
        'carbs_chart_json': carbs_chart_json,
        'fat_chart_json': fat_chart_json,
    }
    return render(request, 'tracker/dashboard.html', context)