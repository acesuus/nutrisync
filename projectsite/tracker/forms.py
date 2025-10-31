from django import forms
from .models import FoodLog

class FoodLogForm(forms.ModelForm):
    # Add natural language query field
    natural_query = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'E.g., "Last night we ordered a 14oz prime rib and mashed potatoes"',
            'rows': 2,
        }),
        label='Describe what you ate (AI-powered)',
        help_text='Describe your meal naturally and we\'ll extract the details automatically'
    )
    
    class Meta:
        model = FoodLog
        fields = ['food_name', 'meal_type', 'date', 'description', 'calories']
        
        widgets = {
            'food_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chicken Salad',
            }),
            'meal_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes about this meal...',
                'rows': 3,
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-filled from API',
                'readonly': 'readonly',
            }),
        }
        
        labels = {
            'food_name': 'Food Name',
            'meal_type': 'Meal Type',
            'date': 'Date',
            'description': 'Nutrition Details',
            'calories': 'Total Calories',
        }
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        from django.utils import timezone
        if date and date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date