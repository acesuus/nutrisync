from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FoodLog(models.Model):
    """
    Model to track food consumption logs with nutrition details
    """
    
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    food_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    calories = models.FloatField(default=0)
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='snack'
    )
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Store detailed nutrition as JSON
    nutrition_data = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Logs'
    
    def __str__(self):
        return f"{self.food_name} - {self.get_meal_type_display()} ({self.date})"
    
    def get_nutrition_value(self, key, default=0):
        """
        Helper method to safely get nutrition values
        """
        if self.nutrition_data and isinstance(self.nutrition_data, dict):
            return self.nutrition_data.get(key, default)
        return default
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Food Log"
        verbose_name_plural = "Food Logs"