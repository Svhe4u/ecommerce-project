from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('order-complete/', views.order_complete, name="order_complete"),
    path('product/<int:id>/', views.product_detail, name="product_detail"),
    path('store/<slug:category_slug>/', views.store_by_category, name="store_by_category"),
    path('store/<slug:category_slug>/<slug:product_slug>/', views.product_detail_by_slug, name="product_detail_by_slug"),
    path('register/', views.register, name="register"),
    path('search/', views.search_result, name="search_result"),
    path('search/store/', views.search, name="store_search"),
    path('review/<int:product_id>/', views.submit_review, name="submit_review"),
    path('signin/', views.signin, name="signin"),
    path('store/', views.store, name="store"),
    path('lab3/', views.lab3, name="lab3"),
]         