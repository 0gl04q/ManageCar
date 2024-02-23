from django import forms
from .models import Car, CarParam


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'gos_number', 'car_model', 'owner', 'mileage', 'year', 'active']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'gos_number': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'car_model': forms.Select(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'owner': forms.Select(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'mileage': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'year': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'active': forms.CheckboxInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            )
        }


class CarParametersForm(forms.ModelForm):
    class Meta:
        model = CarParam
        fields = ['insurance', 'technical_service', 'grm']
        widgets = {
            'insurance': forms.DateInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),

            'technical_service': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
            'grm': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0'
                }
            ),
        }
