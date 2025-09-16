from django.shortcuts import render, redirect
from product_app.models import Item, Category
from product_app.forms import ItemForm
from product_app import forms

# Create your views here.
def index(request):
    item_list = Item.objects.all()
    item_dictionary = {'items': item_list}
    return render(request, 'product_app/index.html', context=item_dictionary)
def itemAdd(request):
    itemForm = forms.ItemForm()
    if request.method == 'POST':
        itemForm_req = forms.ItemForm(request.POST)
        if itemForm_req.is_valid():
            mv = Item.objects.get_or_create(
                name=itemForm_req.cleaned_data['name'],
                price=itemForm_req.cleaned_data['price'],
                category=itemForm_req.cleaned_data['category'])[0]
            mv.save()
        return redirect('index')
    return render(request, 'product_app/product_add.html',{'itemForm':itemForm})