# Generated by Django 5.0.6 on 2024-06-21 08:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_product_composition_remove_product_prodapp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discription',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
