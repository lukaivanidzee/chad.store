from django.urls import path
from products.views import ProductViewSet, ReviewViewSet, FavoriteProductViewSet, CartViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view(), name="products"),
    path('products/<int:pk>/', ProductViewSet.as_view(), name='product'),
    path('reviews/', ReviewViewSet.as_view(), name='review'),
    path('favorite_products/', FavoriteProductViewSet.as_view(), name='favorite_products'),
    path('favorite_products/<int:pk>/', FavoriteProductViewSet.as_view(), name='favorite_product'),
    path('cart/', CartViewSet.as_view(), name='cart')
]