from django import forms
from .models import DailyCheck


class DailyCheckForm(forms.ModelForm):
    class Meta:
        model = DailyCheck
        fields = ['defect', 'defect_status', 'mileage', 'key', 'document']
