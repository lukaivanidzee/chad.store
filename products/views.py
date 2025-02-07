from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from products.models import Product, Cart, ProductTag, FavoriteProduct
from products.serializers import ProductSerializer, ReviewSerializer, CartSerializer, ProductTagSerializer, FavoriteProductSerializer


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({"id": product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProductDetailView(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        obj = get_object_or_404(Product, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        product = get_object_or_404(Product, id=product_id)

        if not isinstance(quantity, int) or quantity <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class ProductTagView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        tags = ProductTag.objects.filter(product=product)
        serializer = ProductTagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        tag_name = request.data.get("tag_name")

        if not tag_name:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        tag, created = ProductTag.objects.get_or_create(product=product, tag_name=tag_name)

        return Response(ProductTagSerializer(tag).data, status=status.HTTP_201_CREATED)


class FavoriteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteProduct.objects.filter(user=request.user)
        serializer = FavoriteProductSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        favorite, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)

        return Response(FavoriteProductSerializer(favorite).data, status=status.HTTP_201_CREATED)