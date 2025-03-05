from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from products.models import Product
import random
from products.choices import Currency

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        faker = Faker()
        product_to_create = []
        currency_data = [
            Currency.EURO,
            Currency.GEL,
            Currency.USD
        ]

        for _ in range(1000):
            name = faker.name()
            description = faker.text()
            price = round(random.uniform(1, 1000), 2)
            currency =  random.choice(currency_data)
            quantity = random.randint(1, 100)

            product = Product(
                name=name,
                description=description,
                price=price,
                currency=currency,
                quantity=quantity
            )
            product_to_create.append(product)

        Product.objects.bulk_create(product_to_create, batch_size=100)
        print(f'Created {len(product_to_create)} products')