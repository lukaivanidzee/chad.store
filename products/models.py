from django.db import models
from config.model_utiles.models import TieStampModel
from products.choices import Currency
from django.core.validators import MaxValueValidator

class Product(TieStampModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return self.name

class Review(TieStampModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL)
    product = models.ForeignKey('Products.product', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return self.product

class ProductTag(TieStampModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='product_tags')

    def __str__(self):
        return self.name