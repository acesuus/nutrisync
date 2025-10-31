from django.db.models import Count, Q
from datetime import timedelta, date
from .models import FoodLog


def get_date_range_logs(start_date=None, end_date=None, meal_type=None):
    """
    Get food logs filtered by date range and meal type.

    Args:
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
        meal_type: Meal type to filter by (optional)

    Returns:
        QuerySet of filtered FoodLog objects
    """
    logs = FoodLog.objects.all()

    if start_date:
        logs = logs.filter(date__gte=start_date)
    if end_date:
        logs = logs.filter(date__lte=end_date)
    if meal_type:
        logs = logs.filter(meal_type=meal_type)

    return logs


def calculate_weekly_summary(end_date=None):
    """
    Calculate summary of logs for the last 7 days.

    Args:
        end_date: End date for the week (defaults to today)

    Returns:
        List of dictionaries with date and count
    """
    if not end_date:
        end_date = date.today()

    start_date = end_date - timedelta(days=6)
    summary = []
    current_date = start_date

    while current_date <= end_date:
        count = FoodLog.objects.filter(date=current_date).count()
        summary.append({
            'date': current_date.strftime('%m/%d'),
            'count': count
        })
        current_date += timedelta(days=1)

    return summary


def get_meal_type_distribution(queryset=None):
    """
    Get distribution of meals by type.

    Args:
        queryset: FoodLog queryset (defaults to all logs)

    Returns:
        List of dictionaries with meal_type and count
    """
    if queryset is None:
        queryset = FoodLog.objects.all()

    distribution = queryset.values('meal_type').annotate(
        count=Count('id')
    ).order_by('-count')

    return list(distribution)


def get_most_frequent_meal_type(queryset=None):
    """
    Find the most frequently logged meal type.

    Args:
        queryset: FoodLog queryset (defaults to all logs)

    Returns:
        Dictionary with meal_type and count, or None
    """
    distribution = get_meal_type_distribution(queryset)
    return distribution[0] if distribution else None


def calculate_statistics(queryset=None):
    """
    Calculate comprehensive statistics for food logs.

    Args:
        queryset: FoodLog queryset (defaults to all logs)

    Returns:
        Dictionary with various statistics
    """
    if queryset is None:
        queryset = FoodLog.objects.all()

    total_logs = queryset.count()
    if total_logs == 0:
        return {
            'total_logs': 0,
            'avg_logs_per_day': 0,
            'most_frequent_meal': None,
            'date_range_start': None,
            'date_range_end': None,
        }

    # Get date range
    date_range_start = queryset.order_by('date').first().date
    date_range_end = queryset.order_by('-date').first().date
    total_days = (date_range_end - date_range_start).days + 1

    # Calculate averages
    avg_logs_per_day = total_logs / total_days if total_days > 0 else 0

    # Get most frequent meal
    most_frequent_meal = get_most_frequent_meal_type(queryset)

    return {
        'total_logs': total_logs,
        'avg_logs_per_day': round(avg_logs_per_day, 1),
        'most_frequent_meal': most_frequent_meal,
        'date_range_start': date_range_start,
        'date_range_end': date_range_end,
    }


def prepare_chart_data(queryset=None, days=7):
    """
    Prepare data for Chart.js visualization.

    Args:
        queryset: FoodLog queryset (defaults to all logs)
        days: Number of days to include in daily chart

    Returns:
        Dictionary with chart data
    """
    if queryset is None:
        queryset = FoodLog.objects.all()

    # Daily data for line chart
    daily_data = calculate_weekly_summary()

    # Meal type distribution for pie chart
    meal_distribution = get_meal_type_distribution(queryset)

    return {
        'daily_counts': daily_data,
        'meal_distribution': meal_distribution,
    }