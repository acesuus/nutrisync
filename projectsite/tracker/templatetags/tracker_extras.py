from django import template

register = template.Library()

@register.filter
def meal_badge_color(meal_type):
    """Return Bootstrap color class for meal type badge"""
    colors = {
        'breakfast': 'warning',
        'lunch': 'info',
        'dinner': 'success',
        'snack': 'secondary',
    }
    return colors.get(meal_type, 'secondary')


@register.filter
def nutrition_percentage(current, target):
    """Calculate percentage of nutrition goal achieved"""
    if not target or target == 0:
        return 0
    percentage = (current / target) * 100
    return min(round(percentage), 100)  # Cap at 100%


@register.filter
def nutrition_bar_color(percentage):
    """Return color class based on percentage achieved"""
    if percentage >= 100:
        return 'success'
    elif percentage >= 75:
        return 'info'
    elif percentage >= 50:
        return 'warning'
    else:
        return 'danger'


# Daily nutrition targets (recommended daily values)
DAILY_TARGETS = {
    'protein_g': 50,  # grams
    'carbohydrates_total_g': 275,  # grams
    'fat_total_g': 78,  # grams
    'fiber_g': 28,  # grams
    'sodium_mg': 2300,  # milligrams
    'potassium_mg': 3500,  # milligrams
    'cholesterol_mg': 300,  # milligrams
}

@register.simple_tag
def get_nutrition_target(nutrient):
    """Get daily target for a specific nutrient"""
    return DAILY_TARGETS.get(nutrient, 0)