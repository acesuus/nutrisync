from django import forms
from .models import FoodLog
from django.contrib.auth.models import User

class FoodLogForm(forms.ModelForm):
    # Add natural language query field
    natural_query = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'E.g., "Last night we ordered a 14oz prime rib and mashed potatoes"',
            'rows': 3,
        }),
        label='Describe what you ate: ',
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


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }
        
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }


class UserSettingsForm(forms.ModelForm):
    """Form for updating user settings"""
    
    # Add custom fields for nutrition goals
    calorie_goal = forms.IntegerField(
        required=False,
        initial=2000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '2000',
            'min': '1000',
            'max': '5000',
        }),
        label='Daily Calorie Goal (kcal)',
        help_text='Your target daily calorie intake'
    )
    
    protein_goal = forms.IntegerField(
        required=False,
        initial=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '50',
            'min': '0',
            'max': '300',
        }),
        label='Daily Protein Goal (g)',
        help_text='Your target daily protein intake'
    )
    
    carbs_goal = forms.IntegerField(
        required=False,
        initial=275,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '275',
            'min': '0',
            'max': '500',
        }),
        label='Daily Carbs Goal (g)',
        help_text='Your target daily carbohydrate intake'
    )
    
    fat_goal = forms.IntegerField(
        required=False,
        initial=78,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '78',
            'min': '0',
            'max': '200',
        }),
        label='Daily Fat Goal (g)',
        help_text='Your target daily fat intake'
    )
    
    class Meta:
        model = User
        fields = ['email']
        
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }
        
        labels = {
            'email': 'Email Address',
        }