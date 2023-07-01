from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime, time
from django.core.mail import send_mail
import stripe
import json
import time
from .models import *

def home(request):
    """ 
    Main page for the website
    """
    
    #get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return render(request, 'store/home.html', {"cart_items": 0})
    
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    except:
        HttpResponse(404, "Object not found")
    
    products = Product.objects.all()
    context = {
        "products": products,
        "cart_items": cart_items,
        }
    return render(request, 'store/home.html', context)

def reviews(request):
    #get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
    
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    except:
        HttpResponse(404, "Object not found")
    
    products = Product.objects.all()
    context = {
        "cart_items": cart_items,
        }
    return render(request, 'store/reviews.html', context)

def user_guide(request):
    #get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
    
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    except:
        HttpResponse(404, "Object not found")
    
    products = Product.objects.all()
    context = {
        "cart_items": cart_items,
        }
    return render(request, 'store/user_guide.html', context)

def faq(request):
    #get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
    
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    except:
        HttpResponse(404, "Object not found")
    
    products = Product.objects.all()
    context = {
        "cart_items": cart_items,
        }
    return render(request, 'store/faq.html', context)

def shop(request):
    
    # get each product
    try:
        blender_white = Product.objects.get(color="White")
        blender_black = Product.objects.get(color="Black")
        blender_pink = Product.objects.get(color="Pink")
        blender_yellow = Product.objects.get(color="Yellow")
    except:
        HttpResponse(404, "Object not found")
    
    context = {
        "blender_white": blender_white,
        "blender_black": blender_black,
        "blender_pink": blender_pink,
        "blender_yellow": blender_yellow,
        "first": True,
    }
    
    #get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
    
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    except:
        HttpResponse(404, "Object not found")

    context = {
        "blender_white": blender_white,
        "blender_black": blender_black,
        "blender_pink": blender_pink,
        "blender_yellow": blender_yellow,
        "cart_items": cart_items,
        "stripe_key": settings.STRIPE_PUBLIC_KEY,
    }
    
    return render(request, 'store/shop.html', context)

def cart(request):
    """ 
    Cart page for each user
    """
    

    # get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
        
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
        items = order.orderitem_set.all()
    except:
        HttpResponse(404, "Object not found")
    
    
    num_items = 0
    for item in items:
        num_items += item.quantity
        
    total = 0
    for order_item in items:
        total += (order_item.product.price * order_item.quantity)
        
    shipping_price = 50 - total
    
    context = {
        "items": items,
        "order": order,
        "num_items": num_items,
        "total_price": total,
        "shipping_price": shipping_price,
        "cart_items": cart_items,
        }
    
    
    return render(request, 'store/cart.html', context)

def checkout(request):
    """ 
    Checkout page for each user
    """
    
    # get customer
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
        
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
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
            
    #Shipping options
    shipping = [{
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 199, "currency": "gbp"},
                    "display_name": "Standard",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 3},
                    },
                },
                }
                ]
    
    if datetime.now().strftime("%H:%M:%S") < "10:00:00":
        shipping.append({
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 399, "currency": "gbp"},
                    "display_name": "Next day (Before 10am)",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 1},
                    },
                },
                })
    
    
    
    
    # post checkout request
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            shipping_options=shipping,
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
    quantity = data['quantity']
    
    # print("Action: " + action)
    # print("Product ID: " + product_id)
    # print("Quantity: " + quantity)

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
        order_item.quantity += int(quantity)
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

def shipping_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        
        # get the logged in customer
        try:
            customer = request.user.customer
        # create customer based on device cookie
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        
        # set customers name and email address
        customer.name = name
        customer.email = email
        customer.save()

        # if shipping details slready exist, delete them
        try:
            ShippingAddress.objects.get(customer=customer).delete()
        except ShippingAddress.DoesNotExist:
            pass
        
        # get customer's order
        try:
            order = Order.objects.get(customer=customer, complete=False)
        except Order.DoesNotExist:
            return HttpResponse(404, "Object not found")
            
        # create new shipping address with given details
        new_shipping = ShippingAddress.objects.create(customer=customer, order=order)
        new_shipping.address = address
        new_shipping.city = city
        new_shipping.state = state
        new_shipping.zipcode = zipcode
        new_shipping.country = country
        new_shipping.save()

        return JsonResponse({
                'data': 'Shipping details saved',
                }, safe=False)

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    
    # get the logged in customer
    try:
        customer = request.user.customer
    # create customer based on device cookie
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return redirect('/')
    user_payment = UserPayment.objects.get(customer=customer)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    
    # get order
    try:
        order = Order.objects.get(customer=customer, complete=False)
    except:
        HttpResponse(404, "Order not found")
        
    # get shipping
    try:
        shipping = ShippingAddress.objects.get(customer=customer)
    except:
        HttpResponse(404, "Shipping not found")
        
    # email shipping
    email_subject = "Smootie Order"
    customer_name = str(customer.name)
    customer_email = str(customer.email)
    # TODO: Delete if not needed
    customer_shipping = {
        "Address": shipping.address,
        "City": shipping.city,
        "State": shipping.state,
        "ZIPCode": shipping.zipcode,
        "Country": shipping.country
    }
    
    order_msg = ""
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        order_msg += "Product: " + str(item.product.name) + "\n" + "Colour: " + str(item.product.color) + "\n" + "Quantity: " + str(item.quantity) + "\n\n"
    
    send_mail(
        email_subject,
        "Order Number: " + str(order.pk) + "\n" +
        "Customer Name: " + str(customer_name) + "\n" +
        "Customer Email: " + str(customer_email) + "\n" +
        "Address: " + str(shipping.address) + "\n" +
        "City: " + str(shipping.city) + "\n" +
        "State: " + str(shipping.state) + "\n" +
        "ZIPCode: " + str(shipping.zipcode) + "\n" +
        "Country: " + str(shipping.country) + "\n\n\n" +
        order_msg,
        
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_RECEIVE_USER],
        fail_silently=False,
    )
    
    # complete order and clear cart
    order.complete = True
    order.save()
    
    
    return render(request, 'store/payment_successful.html', {'customer': customer, 'order': order.pk})

def payment_cancelled(request):
    return render(request, 'store/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
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