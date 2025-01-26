from django.contrib import admin

from products.models import Product, Review, ProductTag, Cart, FavoriteProduct, ProductImage

admin.site.register(ProductTag)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(FavoriteProduct)
admin.site.register(ProductImage)

class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]