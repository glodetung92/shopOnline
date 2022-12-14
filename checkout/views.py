from django.shortcuts import render
from .models import BillingForm
from cart.models import Order
import stripe
from django.conf import settings

def checkout(request):

	# Check out view
	form = BillingForm

	order_qs = Order.objects.filter(user=request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals()
	context = {
		"form": form,
		"order_items": order_items,
		"order_total": order_total
	}

	return render(request, 'checkout/index.html', context)

	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user=request.user)
	if saved_address.exists():
		savedAddress = saved_address.first()
		context = {"form": form, "order_items": order_items, "order_total": order_total, "saveAddress": savedAddress}
	if request.method == 'POST':
		saved_address = BillingAddress.objects.filter(user=request.user)
		if saved_address.exists():
			savedAddress = saved_address.first()
			form = BillingForm(request.POST, instance=savedAddress)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
		else:
			form = BillingForm(request.POST)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				bilingaddress.save()
	return render(request, 'checkout/index.html', context)


def payment(request):
	key = settings.STRIPE_PULISHABLE_KEY
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	order_total = order_qs[0].get_totals()
	totalCents = float(order_total * 100)
	total = round(totalCents, 2)
	if request.method == 'POST':
		charge = stripe.Charge.create(
			amount=total,
			currency = 'usd',
			description = order_qs,
			source = request.POST['stripeToken']
		)
	return render(request, 'checkout/payment.html', {"key": key, "total": total})
