from django import template

register = template.Library()

@register.filter(name='meal_badge_color')
def meal_badge_color(meal_type):
    colors = {
        'breakfast': 'warning',
        'lunch': 'success',
        'dinner': 'primary',
        'snack': 'info',
    }
    return colors.get(meal_type, 'secondary')

@register.filter(name='total_calories')
def total_calories(queryset):
    """
    Calculate total calories from a queryset of FoodLog objects
    """
    total = sum(log.calories or 0 for log in queryset)
    return f"{total:,.0f}"