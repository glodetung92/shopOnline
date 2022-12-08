from django import template
from cart.models import Cart

register = template.Library()

@register.filter(name="cart")

def cart_total(user):
	cart = Cart.objects.filter(user=user)

	if cart.exists():
		return cart.count()
	else:
		return 0
