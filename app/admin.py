from django.contrib import admin
from .models import Customer, Product,Cart,Order

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discount_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'zipcode', 'province']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity', 'product']

@admin.register(Order)
class Payment(admin.ModelAdmin):
    list_display = ['id', 'user', 'Customer', 'product', 'quantity', 'ordered_date', 'status']