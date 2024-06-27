from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Cart, Customer,Order
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        titles = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals()) #{'products': product, 'titles': titles})

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        titles = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals()) 

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm
        return render(request, 'app/Customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"user Register successfully")
        else:
            messages.warning(request,"Invalid input Data")
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,city=city,mobile=mobile,province=province,zipcode=zipcode)
            reg.save()
            messages.success(request,"user Register successfully")
        else:
            messages.warning(request,"Invalid input Data")
        return render(request, 'app/profile.html',locals())

def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
   
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.province = form.cleaned_data['province']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"user info Updated successfully")
        else:
            messages.warning(request,"Invalid input Data")

        return redirect("address")
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    # Remove trailing slash if it exists
    if product_id.endswith('/'):
        product_id = product_id[:-1]

    # Ensure the product_id is an integer
    try:
        product_id = int(product_id)
    except ValueError:
        messages.error(request, "Invalid product ID.")
        return redirect("/")

    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart= Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount + value
    totalamount = amount + 150
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        famount=0
        for p in cart:
            value = p.quantity * p.product.discount_price
            famount = famount + value
        totalamount = famount + 150
        
        return render(request, 'app/checkout.html',locals())

def ordersuccess(request):
    return render(request, 'app/payment_success.html')     

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value

        totalamount = amount + 150

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }

        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value

        totalamount = amount + 150

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        print(prod_id)
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value

        totalamount = amount + 150

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        details = json.loads(request.POST.get('details'))
        customer_id = request.POST.get('custid')
        total_amount = request.POST.get('totalamount')

        try:
            customer = Customer.objects.get(id=customer_id, user=user)
            cart_items = Cart.objects.filter(user=user)

            for item in cart_items:
                Order.objects.create(
                    user=user,
                    Customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    status='Pending'
                )

            cart_items.delete()  # Clear the cart after order creation

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

