from django.db import models


CATEGORY_CHOICES =(
    ('MN','Men'),
    ('WM','Women'),
    ('KD','Kid'),

)
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discription = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image =models.ImageField(upload_to='product')
    def __str__(self):
        return self.title