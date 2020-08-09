from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}