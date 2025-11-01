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


def home(request):
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
        'calories': 0
    }
    
    for log in todays_logs:
        if log.nutrition_data:
            nutrition_totals['protein'] += float(log.nutrition_data.get('protein_g', 0))
            nutrition_totals['carbs'] += float(log.nutrition_data.get('carbohydrates_total_g', 0))
            nutrition_totals['fat'] += float(log.nutrition_data.get('fat_total_g', 0))
            nutrition_totals['fiber'] += float(log.nutrition_data.get('fiber_g', 0))
            nutrition_totals['sodium'] += float(log.nutrition_data.get('sodium_mg', 0))
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


def add_food_log(request):
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


def edit_food_log(request, pk):
    """Edit an existing food log.    
    GET: Display pre-filled form    
    POST: Update the food log"""    
    # Get the food log or return 404 if not found    
    food_log = get_object_or_404(FoodLog, pk=pk)
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


def delete_food_log(request, pk):
    """Delete a food log with confirmation.    
    GET: Show confirmation page    
    POST: Delete the food log"""    
    food_log = get_object_or_404(FoodLog, pk=pk)
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


def dashboard(request):
    """
    Dashboard showing all food logs with:
    - Date range filtering
    - Statistics
    - Charts data
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    meal_filter = request.GET.get('meal_type', '')

    # Filter food logs (you can customize filters here)
    food_logs = FoodLog.objects.all()

    # Use utility functions to compute stats and chart data
    stats = calculate_statistics(food_logs)
    chart_data = prepare_chart_data(food_logs)

    if start_date:
        food_logs = food_logs.filter(date__gte=start_date)
    if end_date:
        food_logs = food_logs.filter(date__lte=end_date)
    if meal_filter:
        food_logs = food_logs.filter(meal_type=meal_filter)

    total_logs = food_logs.count()

    meal_type_counts = food_logs.values('meal_type').annotate(
        count=Count('id')
    ).order_by('-count')

    if food_logs.exists():
        date_range_start = food_logs.order_by('date').first().date
        date_range_end = food_logs.order_by('-date').first().date
        total_days = (date_range_end - date_range_start).days + 1
        avg_logs_per_day = total_logs / total_days if total_days > 0 else 0
    else:
        date_range_start = None
        date_range_end = None
        avg_logs_per_day = 0

    most_frequent_meal = meal_type_counts.first() if meal_type_counts else None

    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_counts = [
        {
            'date': day.strftime('%m/%d'),
            'count': FoodLog.objects.filter(date=day).count()
        }
        for day in last_7_days
    ]

    meal_distribution = list(meal_type_counts)
    daily_counts_json = json.dumps(daily_counts)
    meal_distribution_json = json.dumps(meal_distribution)

    context = {
        **stats,
        **chart_data,
        'food_logs': food_logs,
        'total_logs': total_logs,
        'meal_type_counts': meal_type_counts,
        'most_frequent_meal': most_frequent_meal,
        'avg_logs_per_day': round(avg_logs_per_day, 1),
        'date_range_start': date_range_start,
        'date_range_end': date_range_end,
        'daily_counts': daily_counts,
        'meal_distribution': meal_distribution,
        'start_date': start_date,
        'end_date': end_date,
        'meal_filter': meal_filter,
        'daily_counts_json': daily_counts_json,
        'meal_distribution_json': meal_distribution_json,
    }
    return render(request, 'tracker/dashboard.html', context)