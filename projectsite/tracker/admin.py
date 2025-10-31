from django.contrib import admin
from .models import FoodLog

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'meal_type', 'date', 'calories', 'created_at']
    list_filter = ['meal_type', 'date']
    search_fields = ['food_name', 'description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Meal Information', {
            'fields': ['food_name', 'meal_type', 'date', 'calories']
        }),
        ('Additional Notes', {
            'fields': ['description'],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]