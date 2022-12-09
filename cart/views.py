from django.shortcuts import render, redirect
from products.models import Product
from cart.models import Cart, Order
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Add To Cart View
def add_to_cart(request, slug):
	# Lay item theo slug ( truyen slug nhu la parameter)
	item = get_object_or_404(Product, slug=slug)
	# Tao moi hoac get cart ( Neu chua co thi create, neu co roi thi get)
	order_item, created = Cart.objects.get_or_create(
		item = item,
		user = request.user
	)
	# check xem coi nguoi dung da co order nao ma chua send khong
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	# Neu co order chua send roi thi push item trong card do vao order 
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.orderitems.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "This item quantity was updated.")
			return redirect('mainapp:home')
		# Neu item do chua co trong order
		else:
			order.orderitems.add(order_item)
			messages.info(request, "This item was added to your cart.")
			return redirect('mainapp:home')
	# Neu chua co no se tao 1 Order moi cho nguoi dung hien tai
	else:
		order = Order.objects.create(
			user=request.user,
		)
		# After push order item to new createad order
		order.orderitems.add(order_item)
		messages.info(request, "This is was added to your cart.")
		return redirect('mainapp:home')

# Remove item from cart
def remove_from_cart(request, slug):
	# Get item based on slug ( if not return 404 )
	item = get_object_or_404(Product, slug=slug)
	# Check cart of now user 
	cart_qs = Cart.objects.filter(user=request.user, item=item)
	# if cart is isset check item in that cart
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


# cart view
def CartView(request):

	user = request.user

	carts = Cart.objects.filter(user=user)
	orders = Order.objects.filter(user=user, ordered=False)

	content = {
		"carts": carts,
		"order": orders[0]
	}

	if carts.exists():
		return render(request, 'cart/home.html', content)
	else:
		messages.warning(request, "You do not have an active order")
		return redirect("mainapp:home")

def decreaseCart(request, slug):
	item = get_object_or_404(Product, slug=slug)

	order_qs = Order.objects.filter(
		user = request.user,
		ordered = False
	)

	if order_qs.exists():
		order = order_qs[0]
		# check if order item is in order
		if order.orderitems.filter(item__slug = item.slug).exists():
			order_item = Cart.objects.filter(
				item = item,
				user = request.user
			)[0]
			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.orderitems.remove(order_item)
				order_item.delete()
			messages.info(request, f"{item.name} quantity has updated.")
			return redirect("mainapp:cart-home")
		else:
			messages.info(request, f"{item.name} quantity has updated.")
			return redirect("mainapp:cart-home")
	else:
		messages.info(request, "you do not have an active order")
		return redirect("mainapp:cart-home")



def increaseCart(request, slug):
	# Lay item theo slug ( truyen slug nhu la parameter)
	item = get_object_or_404(Product, slug=slug)

	order_item,created = Cart.objects.get_or_create(
		item = item,
		user = request.user,
	)

	# check xem coi nguoi dung da co order nao ma chua send khong
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	# Neu co order chua send roi thi push item trong card do vao order 
	if order_qs.exists():
		order = order_qs[0]
		# check if the order item is in the order
		if order.orderitems.filter(item__slug=item.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, f"{item.name} quantity has updated.")
			return redirect('mainapp:cart-home')
		# Neu item do chua co trong order
		else:
			order.orderitems.add(order_item)
			messages.info(request, "This item was added to your cart.")
			return redirect('mainapp:cart-home')
	# Neu chua co no se tao 1 Order moi cho nguoi dung hien tai
	else:
		order = Order.objects.create(
			user=request.user,
		)
		# After push order item to new createad order
		order.orderitems.add(order_item)
		messages.info(request, "This is was added to your cart.")
		return redirect('mainapp:home')


