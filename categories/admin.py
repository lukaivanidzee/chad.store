from django.contrib import admin
from categories.models import Category, CategoryImage

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1

@admin.register(Category)
class CategoryAmin(admin.ModelAdmin):
    inlines = [CategoryImageInline]