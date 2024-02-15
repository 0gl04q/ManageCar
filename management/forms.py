from django import forms
from .models import DailyCheck
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _


class DailyCheckForm(forms.ModelForm):

    photo_1 = forms.ImageField(widget=forms.FileInput(
        attrs={
            'onchange': "handleFileChange('id_photo_1', 'photoStatus_1')",
            'capture': 'camera',
            'style': 'opacity: 0; position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: pointer;'
        }
    ))
    photo_2 = forms.ImageField(widget=forms.FileInput(
        attrs={
            'onchange': "handleFileChange('id_photo_2', 'photoStatus_2')",
            'capture': 'camera',
            'style': 'opacity: 0; position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: pointer;'
        }
    ))

    class Meta:
        model = DailyCheck
        fields = ['photo_1', 'photo_2', 'defect', 'defect_status', 'mileage_auto', 'mileage_daily', 'document', 'location']
        widgets = {
            'defect': forms.Textarea(
                attrs={
                    'class': 'col-6 text-center border-0',
                    'placeholder': 'Опишите наличие дефектов',
                    'rows': 2
                }
            ),
            'defect_status': forms.Select(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0',
                }
            ),
            'mileage_auto': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0',
                    'placeholder': 'Напишите общий пробег'
                }
            ),
            'mileage_daily': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0',
                    'placeholder': 'Напишите дневной пробег'
                }
            ),
            'document': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0',
                    'placeholder': 'Расположение документов/ключей'
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'col-6 align-self-center text-center border-0',
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
            },
            'photo_1': {
                'required': 'Введите число'
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
