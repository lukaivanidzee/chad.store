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
    class Meta:
        model = Cart
        fields = ["id", "user", "product", "quantity"]

    # პროდუქტის რაოდენობა უნდა იყოს 1 ან მეტი
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = ["id", "user", "product"]

    # პროდუქტი უნდა არსებობდეს მონაცემთა ბაზაში 
    def validate_product(self, value):
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("This product does not exist")
        return value


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["id", "product", "tag_name"]

    # თაგის სახელი არ უნდა იყოს ცარიელი და უნდა იყოს უნიკალური
    def validate_tag_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Tag name cannot be empty.")
        return value