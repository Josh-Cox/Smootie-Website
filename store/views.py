from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json
import time
from .models import *

def home(request):
    """ 
    Main page for the website
    """
    
    # if user is logged in return cart items
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }
        cart_items = order['get_cart_items']
    
    products = Product.objects.all()
    context = {
        "products": products,
        "cart_items": cart_items,
        }
    return render(request, 'store/home.html', context)

def user_guide(request):
    return render(request, 'store/user_guide.html')

def faq(request):
    return render(request, 'store/faq.html')

def cart(request):
    """ 
    Cart page for each user
    """

    # get customer
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        
    else:
        items = []
        order = {
            "get_cart_total": 0,
            "get_cart_items": 0,
        }
        
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    
    num_items=  0
    for item in items:
        num_items += item.quantity
    
    context = {
        "items": items,
        "order": order,
        "num_items": num_items,
        }
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    """ 
    Checkout page for each user
    """
    
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    
    # post checkout request
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        
        return redirect(checkout_session.url, code=303)
    
    # if user is logged in return checkout items
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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

def update_item(request):
    """
    Add/remove an item to/from the cart
    """
    
    
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    
    print("Action: " + action)
    print("Product ID: " + product_id)

    # get the logged in customer
    try:
        customer = request.user.customer
    # create customer based on device cookie
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    
    # get the selected product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse('Object not found', status=404)
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    # check if action is add or remove
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    elif action == 'clear':
        order_item.quantity = 0
    
    # save the item
    order_item.save()
    
    # delete the item from the database
    if order_item.quantity <= 0:
        order_item.delete()
        return JsonResponse({
            'data': 'Item updated',
            'redirect': True,
            }, safe=False)
        
        
    return JsonResponse({
            'data': 'Item updated',
            'redirect': False,
            }, safe=False)


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user = request.user
    customer = Customer.objects.get(user=user)
    user_payment = UserPayment.objects.get(customer=customer)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'store/payment_successful.html', {'customer': customer})

def payment_cancelled(request):
    return render(request, 'store/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse('Invalid payload', status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse('Invalid signature', status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
        
    return HttpResponse(status=200)