# Generated by Django 5.1.5 on 2025-02-16 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_rename_product_categoryimage_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryimage',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
