# from django.shortcuts import render
# from templates import all


# # Create your views here.
# def index(request):
#     return render(request, "index.html")


from django.shortcuts import render
from .models import Product, Category, ImageGallery, ReviewRating
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg

def index(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products,
        'count': products.count(),
    }
    return render(request, "index.html", context)


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


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products": products,
        "products_count": products.count(),
        "categories": categories,
    }
    return render(request, "home.html", context)


def store(request):
    # Use raw SQL to demonstrate alternative querying
    raw_products = Product.objects.raw("SELECT * FROM baraa_tbl")
    products_count = Product.objects.count()
    categories = Category.objects.all()
    context = {
        "products": raw_products,
        "products_count": products_count,
        "categories": categories,
    }
    return render(request, "store.html", context)


def lab3(request):
    products = Product.objects.all()
    return render(request, "lab3.html", {'products': products})


# --- Inserted views based on user's request (adapted to existing models/templates) ---

def store_by_category(request, category_slug=None):
    category = None
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        product_qs = Product.objects.filter(category=category, is_available=True)
    else:
        product_qs = Product.objects.filter(is_available=True)

    paginator = Paginator(product_qs, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = product_qs.count()

    context = {
        'products': paged_products,
        'count': count,
        'category': category,
    }
    return render(request, "store.html", context)


def product_detail_by_slug(request, category_slug, product_slug):
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
    )
    product_gallery = ImageGallery.objects.filter(product_id=product.id)
    rate = ReviewRating.objects.filter(product_id=product.id).aggregate(Avg('rating'))
    comments = ReviewRating.objects.filter(product_id=product.id).select_related('user')

    context = {
        'single_product': product,
        'product_gallery': product_gallery,
        'rate': rate.get('rating__avg'),
        'comments': comments,
    }
    return render(request, "product-detail.html", context)


def search(request):
    kw = request.GET.get('keyword', '').strip()
    if kw:
        products = Product.objects.filter(
            Q(product_name__icontains=kw) | Q(description__icontains=kw)
        )
    else:
        products = Product.objects.none()
    context = {
        'products': products,
        'count': products.count(),
        'kw': kw,
    }
    return render(request, "store.html", context)


def submit_review(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        ReviewRating.objects.create(
            product=product,
            user=request.user,
            title=request.POST.get('title', ''),
            review=request.POST.get('review', ''),
            rating=float(request.POST.get('rate', 0) or 0),
            ip=request.META.get('REMOTE_ADDR', ''),
        )
        return redirect(product.get_url())
    return redirect('store')