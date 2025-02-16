from django.urls import path
from categories.views import CategoryDetailView, CategoryImageView, CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name = 'categories'),
    path('categories/<int:category_id>/images/', CategoryImageView.as_view(), name = 'categories')
]