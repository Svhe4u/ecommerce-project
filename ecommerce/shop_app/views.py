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

def product_detail(request, category_slug, product_slug):
    product = Product.objects.get(category__slug = category_slug, slug=product_slug)
    product_gallery = ImageGallery.objects.filter(product_id = product.id)
    rate = ReviewRating.objects.filter(
        product_id=product.id).aggregate(Avg('rating'))
    con = sql.connect("db.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(f"""SELECT title, review, username, pro_image FROM 
        (auth_user INNER JOIN accounts_account
        ON auth_user.id = accounts_account.user_id) 
        INNER JOIN store_reviewrating
        ON accounts_account.user_id = store_reviewrating.user_id 
        WHERE product_id={product.id}""")

    comments = cur.fetchall()
    
    context = {
        'single_product': product,
        'product_gallery': product_gallery,
        'rate': rate['rating__avg'],
        'comments': comments,
    }

    return render(request, "product_detail.html", context)


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


def store(request, category_slug=None):
    cat = None
    pr = None

    if category_slug != None:
        cate = get_object_or_404(Category, slug=category_slug)
        product_qs = Product.objects.filter(category=cate)
    else:
        product_qs = Product.objects.filter(is_available=True)

    paginator = Paginator(product_qs, 9)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    count = product_qs.count()

    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'count': count,
        'categories': categories,
        'is_paginated': paged_products.has_other_pages(),
        'page_obj': paged_products,
        'paginator': paginator,
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

    paginator = Paginator(product_qs, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = product_qs.count()
    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'count': count,
        'category': category,
        'categories': categories,
        'is_paginated': paged_products.has_other_pages(),
        'page_obj': paged_products,
        'paginator': paginator,
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