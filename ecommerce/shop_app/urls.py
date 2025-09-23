from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('order-complete/', views.order_complete, name="order_complete"),
    path('product/<int:id>/', views.product_detail, name="product_detail"),
    path('register/', views.register, name="register"),
    path('search/', views.search_result, name="search_result"),
    path('signin/', views.signin, name="signin"),
    path('store/', views.store, name="store"),
    path('lab3/', views.lab3, name="lab3"),
]