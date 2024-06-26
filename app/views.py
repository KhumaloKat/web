from django.db.models import Count
from django.shortcuts import render,redirect
from django.views import View
from . models import Product
from . forms import Customer,CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

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
        pass
