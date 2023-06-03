from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user_guide/', views.user_guide, name="user_guide"),
    path('faq/', views.faq, name="faq"),
    path('shop/', views.shop, name="shop"),
    path('reviews/', views.reviews, name="reviews"),
    path('cart/', views.cart, name="cart"),
    path('shipping_submit/', views.shipping_submit, name="shipping_submit"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment_successful/', views.payment_successful, name="payment_successful"),
    path('payment_cancelled/', views.payment_cancelled, name="payment_cancelled"),
    path('stripe_webhook/', views.stripe_webhook, name="stripe_webhook"),
    path('update_item/', views.update_item, name="update_item"),
]