from django import forms
from .models import FoodItem


class FoodItemForm(forms.ModelForm):
    
    class Meta:
        model = FoodItem
        fields = ['name', 'calories']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter food name',
                'required': 'required'
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter calories',
                'min': '0',
                'required': 'required'
            })
        }
        labels = {
            'name': 'Food Name',
            'calories': 'Calories'
        }
    
    def clean_calories(self):
        calories = self.cleaned_data['calories']
        if calories <= 0:
            raise forms.ValidationError("Calories must be a positive number.")
        return calories