from django.urls import path
from products.views import Home
from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart, increaseCart


app_name = 'mainapp'

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('cart/', CartView, name='cart-home'),
	path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
	path('increase-cart/<slug>', increaseCart, name='increase-cart'),
	path('cart/<slug>', add_to_cart, name='cart'),
	path('remove/<slug>', remove_from_cart, name='remove-cart'),
]
