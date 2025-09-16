from django import forms
from django.forms import ModelForm
from product_app.models import Item, Category


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'category']