from django import forms
from .models import DailyCheck


class DailyCheckForm(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['defect', 'defect_status', 'mileage_auto', 'mileage_daily', 'key', 'document']
        widgets = {
            'defect': forms.Textarea(
                attrs={
                    'class': 'form-control mb-1',
                    'placeholder': 'Опишите наличие дефектов',
                    'rows': 5
                }
            ),
            'defect_status': forms.Select(
                attrs={
                    'class': 'form-control mb-1'
                }
            ),
            'mileage_auto': forms.TextInput(
                attrs={
                    "class": "form-control mb-1",
                    'placeholder': 'Напишите общий пробег'
                }
            ),
            'mileage_daily': forms.TextInput(
                attrs={
                    'class': 'form-control mb-1',
                    'placeholder': 'Напишите дневной пробег'
                }
            ),
            'key': forms.TextInput(
                attrs={
                    'class': 'form-control mb-1',
                    'placeholder': 'Напишите местонахождение ключей'
                }
            ),
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'placeholder': 'Напишите местонахождение документов'
                }
            )
        }
        error_messages = {
            'mileage_auto': {
                'invalid': 'Пожалуйста введите общий автопробег числом'
            },
            'mileage_daily': {
                'invalid': 'Пожалуйста введите дневной автопробег числом'
            }
        }


class PhotoForm(forms.Form):
    photo = forms.CharField(widget=forms.HiddenInput)
