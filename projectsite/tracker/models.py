from django.db import models

class FoodLog(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    # Required fields
    food_name = models.CharField(max_length=200)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    
    # Optional fields
    description = models.TextField(blank=True, null=True)
    calories = models.FloatField(null=True, blank=True, help_text="Total calories")
    
    # Automatic timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.food_name} - {self.date}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Food Log"
        verbose_name_plural = "Food Logs"