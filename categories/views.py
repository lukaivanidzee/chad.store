from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from categories.models import Category, CategoryImage
from categories.serializers import CategorySerializer, CategoryDetailSerializer, CategoryImageSerializer

from rest_framework.filters import SearchFilter

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class CategoryImageViewSet(ListCreateAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return self.queryset.filter(category=category_id)