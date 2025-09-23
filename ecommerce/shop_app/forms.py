from django import forms
from .models import *


class BaraaForm(forms.ModelForm):
    class Meta:
        model = Baraa
        fields = '__all__'
        labels = {
            'ner': 'Нэр',
            'une': 'Үнэ',
            'too': 'Тоо ширхэг',
        }