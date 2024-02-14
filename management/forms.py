from django import forms
from .models import DailyCheck
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _


class DailyCheckForm(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['defect', 'defect_status', 'mileage_auto', 'mileage_daily', 'document', 'location']
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
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control mb-1',
                    'placeholder': 'Расположение документов/ключей'
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Напишите стоянку'
                }
            ),
        }
        error_messages = {
            'mileage_auto': {
                'invalid': 'Пожалуйста введите общий автопробег числом'
            },
            'mileage_daily': {
                'invalid': 'Пожалуйста введите дневной автопробег числом'
            }
        }

    def clean_mileage_auto(self):
        mileage_auto = self.cleaned_data['mileage_auto']
        daily_check = self.instance
        if mileage_auto < daily_check.car.mileage:
            raise ValidationError(_('Общий пробег должен быть больше чем текущий'))

        return mileage_auto

    def clean_mileage_daily(self):
        mileage_daily = self.cleaned_data['mileage_daily']
        daily_check = self.instance
        if mileage_daily > daily_check.car.mileage:
            raise ValidationError(_('Дневной пробег должен быть меньше или равен общему пробегу'))

        return mileage_daily


class PhotoForm(forms.Form):
    photo = forms.CharField(widget=forms.HiddenInput)
