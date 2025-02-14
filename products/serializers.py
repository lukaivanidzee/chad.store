from rest_framework import serializers
from products.models import Review, Product, Cart, FavoriteProduct, ProductTag, Product


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['product_id', 'content', 'rating']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.pop('product_id'))
        user = self.context['request'].user
        return Review.objects.create(product=product, user=user, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        exclude = ['created_at', 'updated_at', 'tags'] 
        model = Product


from rest_framework import serializers
from products.models import Cart, FavoriteProduct, ProductTag, Product

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        source = 'products',
        queryset = Product.objects.all(),
        many = True,
        write_only = True
    )
    
    class Meta:
        model = Cart
        fields = ["user", "product_ids", "products"]
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        products = validated_data.pip('products')

        cart, = Cart.objects.get_or_create(user=user)
        cart.products.add(*products)

        return cart



class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product", "product_id"]

    # პროდუქტი უნდა არსებობდეს მონაცემთა ბაზაში 
    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("This product does not exist")
        return value
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = validated_data.pop('user')

        product = Product.objects.get(id=product_id)

        favourite_product, crated = FavoriteProduct.objects.get_or_create(user=user, product=product)

        if not crated:
            raise serializers.ValidationError('This product isalready in Favourite items')
        return favourite_product


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["id", "product", "tag_name"]

    # თაგის სახელი არ უნდა იყოს ცარიელი და უნდა იყოს უნიკალური
    def validate_tag_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Tag name cannot be empty.")
        return value