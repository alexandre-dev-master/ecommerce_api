from django.contrib import admin
from .models import Products, Category

# Register your models here so they appear in the Django Admin
admin.site.register(Products)
admin.site.register(Category)