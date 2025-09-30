# from django.shortcuts import render
# from templates import all


# # Create your views here.
# def index(request):
#     return render(request, "index.html")


from django.shortcuts import render
from .models import Product, Category
from templates import * 

def index(request):
    return render(request, "index.html")


def cart(request):
    return render(request, "cart.html")


def dashboard(request):
    return render(request, "dashboard.html")


def order_complete(request):
    return render(request, "order_complete.html")


def product_detail(request, id):
    return render(request, "product-detail.html", {'id': id})


def register(request):
    return render(request, "register.html")


def search_result(request):
    categories = Category.objects.all()
    query = request.GET.get('q') or ''
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
        "products_count": products.count(),
        "query": query,
    }
    return render(request, "search-result.html", context)


def signin(request):
    return render(request, "signin.html")


def store(request):
    return render(request, "store.html")


def lab3(request):
    products = Product.objects.all()
    return render(request, "lab3.html", {'products': products})