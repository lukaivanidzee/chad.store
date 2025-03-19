# improts
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.exceptions import PermissionDenied

from products.models import (
    Product,
    Review,
    FavoriteProduct,
    Cart, ProductTag, ProductImage, CartItem
)

from products.serializers import (
    ProductSerializer,
    ReviewSerializer,
    FavoriteProductSerializer,
    CartSerializer,
    ProductTagSerializer, ProductImageSerializer, CartItemSerializer
    )

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.pagination import ProductPagination
from products.filters import ProductFilter, ReviewFilter

from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle

from products.permissions import IsObjectOwnerReadOnly
# ____________________________

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    throttling_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['price', 'categories']
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    pagination_class = ProductPagination
    
    
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerReadOnly]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['rating']
    filterset_class = ReviewFilter

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    def perfom_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied('You can not change it')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You can not delete it')
        instance.delete()
    
class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "likes"

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    http_method_names = ['get', 'post', 'delete']
    
class CartViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    
    
class TagList(ListModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    throttling_classes = [UserRateThrottle]

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])

    http_method_names = ['get', 'post', 'delete']


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this item.")
        serializer.save()