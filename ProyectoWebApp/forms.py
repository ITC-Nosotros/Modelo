from django import forms
from .models import CarSelection

class CarForm(forms.ModelForm):
    class Meta:
        model = CarSelection
        fields = [
            'car_choice',
            'location',
            'price_range',
            'km_range',
            'yearmodel_range', 
        ]