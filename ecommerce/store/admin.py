from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')  # name → category_name
    prepopulated_fields = {'slug': ('category_name',)}  # name → category_name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'slug')  # name → product_name
    prepopulated_fields = {'slug': ('product_name',)}  # name → product_name
    list_filter = ('category',)
