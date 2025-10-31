from django import forms
from .models import FoodLog

class FoodLogForm(forms.ModelForm):
    # Add natural language query field
    natural_query = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'E.g., "Last night we ordered a 14oz prime rib and mashed potatoes"',
            'rows': 3,
        }),
        label='Describe what you ate (AI-powered)',
        help_text='Describe your meal naturally and we\'ll extract the details automatically'
    )
    
    class Meta:
        model = FoodLog
        fields = ['meal_type', 'date']
        
        widgets = {
            'meal_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        
        labels = {
            'meal_type': 'Meal Type',
            'date': 'Date',
        }
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        from django.utils import timezone
        if date and date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date