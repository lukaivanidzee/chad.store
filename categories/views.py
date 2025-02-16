from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from categories.serializers import CategoryImageSerializer, CategorDetailSerializer, CategorySerializer
from categories.models import Category, CategoryImage

class CategoryListView(ListModelMixin,  GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CategoryDetailView(RetrieveModelMixin,  GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
class CategoryImageView(ListModelMixin, CreateModelMixin,  GenericAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(category=self.kwargs['category_id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)