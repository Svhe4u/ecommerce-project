from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store_root'),
    path('home/', views.home, name='store_home'),
]



