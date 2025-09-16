from django.shortcuts import render
from templates import all


# Create your views here.
def index(request):
    return render(request, "index.html")