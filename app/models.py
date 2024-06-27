from django.db import models
from django.contrib.auth.models import User

PROVINCE_CHOICES =(
    ('Mpumalanga','Mpumalanga'),
    ('Gauteng','Gauteng'),
    ('KwaZulu Natal','KwaZulu Natal'),
    ('Free State','Free State'),
    ('Western Cape','Western Cape'),
    ('North West','North West'), 
    ('Northen Cape','Northen Cape'),
    ('Limpopo','Limpopo'),
    ('Eastern Cape','Eastern Cape'), 
)
CATEGORY_CHOICES =(
    ('MN','Men'),
    ('WM','Women'),
    ('KD','Kid'),

)

STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),

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
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    province = models.CharField(choices = PROVINCE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


