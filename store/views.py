from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    """ 
    Main page for the website
    """
    
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'store/home.html', context)

def cart(request):
    """ 
    Cart page for each user
    """
    # if user is logged in return cart items
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }
        
    context = {
        "items": items,
        "order": order,
        }
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    """ 
    Checkout page for each user
    """
    
    # if user is logged in return checkout items
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }
        
    context = {
        "items": items,
        "order": order,
        }
    return render(request, 'store/checkout.html', context)