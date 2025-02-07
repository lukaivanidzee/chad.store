from django.urls import path
from products.views import ProductListCreateView, reviews_view, ProductDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name="products"),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('reviews/', reviews_view, name="reviews")
]