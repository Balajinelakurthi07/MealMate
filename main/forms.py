from django import forms

class DishForm(forms.Form):
    dish_name = forms.CharField(
        label='Dish Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the name of the dish',
            'class': 'form-control'
        })
    )

from django import forms
from .models import Order

