from django.shortcuts import render, redirect
from products.models import Product
from cart.models import Cart, Order
from django.shortcuts import get_object_or_404
from django.contrib import messages


# Add To Cart View
def add_to_cart(request, slug):
	item = get_object_or_404(Product, slug=slug)
	order_item, created = Cart.objects.get_or_create(
		item = item,
		user = request.user
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.orderitems.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item quantity was updated.")
			return redirect('mainapp:home')
		else:
			order.orderitems.add(order_item)
			messages.info(request, "This item was added to your cart.")
			return redirect('mainapp:home')
	else:
		order = Order.objects.create(
			user=request.user,
		)
		order.orderitems.add(order_item)
		messages.info(request, "This is was added to your cart.")
		return redirect('mainapp:home')

# Remove item from cart
def remove_from_cart(request, slug):
	item = get_object_or_404(Product, slug=slug)
	cart_qs = Cart.objects.filter(user=request.user, item=item)
	if cart_qs.exists():
		cart = cart_qs[0]
		# Check the cart quantity
		if cart.quantity > 1:
			cart.quantity -= 1
			cart.save()
		else:
			cart_qs.delete()
	order_qs = Order.objects.filter(
		user=request.user,
		ordered = False
	)
	if order_qs.exists():
		order = order_qs[0]
		# Check if the order item is in the order
		if order.orderitems.filter(item__slug=item.slug).exists():
			order_item = Cart.objects.filter(
				item = item,
				user=request.user,
			)[0]
			order.orderitems.remove(order_item)
			messages.info(request, "This item was removed from your cart.")
			return redirect('mainapp:home')
		else:
			messages.info(request, "This item was not in your cart.")
			return redirect('mainapp:home')
	else:
		messages.info(request, "You do not have an active order.")
		return redirect('mainapp:home')