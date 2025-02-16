from rest_framework import serializers
from categories.models import Category, CategoryImage
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['id', 'image', 'is_active', 'category']

class CategorDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    images = CategoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products', 'images']