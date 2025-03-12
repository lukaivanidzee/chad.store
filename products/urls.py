from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from products.views import ProductViewSet, ReviewViewSet, FavoriteProductViewSet, CartViewSet, TagList, ProductImageViewSet, CartItemViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewSet)

products_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)

products_router.register('images', ProductImageViewSet)
products_router.register('reviews', ReviewViewSet)

router.register('favorite_products', FavoriteProductViewSet)
router.register('cart', CartViewSet)
router.register('cart_items', CartItemViewSet, basename='cart-items')
router.register('tag', TagList)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
