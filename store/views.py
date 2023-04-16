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

def shop(request):
    return render(request, 'store/shop.html')

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
        
    total = 0
    for order_item in items:
        total += (order_item.product.price * order_item.quantity)
        
    shipping_price = 45 - total
    
    context = {
        "items": items,
        "order": order,
        "num_items": num_items,
        "total_price": total,
        "shipping_price": shipping_price
        }
    
    print(total)
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    """ 
    Checkout page for each user
    """
    
    # get customer
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    
    white_q = 0
    black_q = 0
    pink_q = 0
    yellow_q = 0
    
    try:
        white_q = OrderItem.objects.get(order=order, product=Product.objects.get(color="White")).quantity
    except:
        pass
    try:
        pink_q = OrderItem.objects.get(order=order, product=Product.objects.get(color="Pink")).quantity
    except:
        pass
    try:
        black_q = OrderItem.objects.get(order=order, product=Product.objects.get(color="Black")).quantity
    except:
        pass
    try:
        yellow_q = OrderItem.objects.get(order=order, product=Product.objects.get(color="Yellow")).quantity
    except:
        pass
    
    # products in cart
    if order.get_cart_total >= 50:
        white_dict = {
            'price': settings.PRODUCT_DISCOUNT_WHITE,
            'quantity': white_q
        }
        
        black_dict = {
        'price': settings.PRODUCT_DISCOUNT_BLACK,
        'quantity': black_q
        }
        
        pink_dict = {
            'price': settings.PRODUCT_DISCOUNT_PINK,
            'quantity': pink_q
        }
        
        yellow_dict = {
            'price': settings.PRODUCT_DISCOUNT_YELLOW,
            'quantity': yellow_q
        }
    else: 
        white_dict = {
            'price': settings.PRODUCT_PRICE_WHITE,
            'quantity': white_q
        }
        
        black_dict = {
        'price': settings.PRODUCT_PRICE_BLACK,
        'quantity': black_q
        }
        
        pink_dict = {
            'price': settings.PRODUCT_PRICE_PINK,
            'quantity': pink_q
        }
        
        yellow_dict = {
            'price': settings.PRODUCT_PRICE_YELLOW,
            'quantity': yellow_q
        }
    
    product_arr = [white_dict, black_dict, pink_dict, yellow_dict]
    
    items = []
    
    for product in product_arr:
        if product['quantity'] > 0:
            items.append(product)
            
    print(items)
    
    # post checkout request
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            shipping_options=[
                {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 199, "currency": "gbp"},
                    "display_name": "Standard",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 3},
                    },
                },
                },
                {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 399, "currency": "gbp"},
                    "display_name": "Next day (Before 10am)",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 1},
                    },
                },
                },
            ],
            line_items = items,
            mode = 'payment',
            customer_creation = 'always',
            success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        
        return redirect(checkout_session.url, code=303)
    

    items = order.orderitem_set.all()
    
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