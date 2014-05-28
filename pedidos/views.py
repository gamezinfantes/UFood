import paypalrestsdk
from carton.cart import Cart
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from restaurante.models import Plato, Restaurante
from UFood.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET




# Create your views here.
def carrito(request):
	cart = Cart(request.session)
	print cart.items[0].product

	return HttpResponse('hola soy un carrito')


def platilla_cesta(request):
	cart = Cart(request.session)
	return render(request, 'pedidos/carrito.html', {'cart': cart})#, content_type="application/json"


def add_single(request):
	cart = Cart(request.session)
	plato = Plato.objects.get(id=request.GET.get('product_id'))

	if cart.products:
		if plato.restaurante.id != cart.products[0].restaurante.id:
			cart.clear()		
	cart.add(plato, price=plato.precio)
	return platilla_cesta(request);

def remove(request):
	cart = Cart(request.session)
	pass

def remove_single(request):
	cart = Cart(request.session)
	pass

def clear(request):
	cart = Cart(request.session)
	pass

def set_queantity(request):
	cart = Cart(request.session)
	pass


def pago(request):
	if request.method == "POST":

		'''

		#
		#	Guardo el pedido
		# ===========================
		
		cart = Cart(request.session)
		# creo un pedido con los datos del cliente y el restaurante
		restaurante = cart.items[0].restaurante
		cliente = Cliente.objects.get(user=request.user) #falta el cliente
		pedido = Pedido (restaurante=restaurante, cliente=cliente)
		pedido.save()
		
		#añado platos al pedido
		for item in cart.items:
			plato = item.product
			Detalle_pedido(plato=plato, pedido=pedido, cantidad=item.quantity).save()
		
		
		#cart.clear() Se vaciará despues porque lo usa para coger los platos del pedido
		'''


		if request.POST.get('pago') == "Paypal":
			return paypal_create(request)
		elif request.POST.get('pago') == "Efectivo":
			return HttpResponseRedirect(reverse('webapp.views.pago_exitoso'))

	return HttpResponseRedirect(reverse('webapp.views.pago_exitoso'))


	


def paypal_create(request):
	cart = Cart(request.session)

	total = str(format(cart.total, '.2f'))
	platos = []

	for item in cart.items:
		plato = item.product
		p = {
			"name": plato.nombre,
			"price": str(format(plato.precio,'.2f')),
			"currency": "EUR",
			"quantity": item.quantity
		}
		platos.append(p)

	paypalrestsdk.configure({
		"mode": PAYPAL_MODE,
		"client_id": PAYPAL_CLIENT_ID,
		"client_secret": PAYPAL_CLIENT_SECRET })
	# ###Payment
	# A Payment Resource; create one using
	# the above types and intent as 'sale'
	payment = paypalrestsdk.Payment({
	  "intent":  "sale",

	  # ###Payer
	  # A resource representing a Payer that funds a payment
	  # Payment Method as 'paypal'
	  "payer":  {
	    "payment_method":  "paypal" },

	  # ###Redirect URLs
	  "redirect_urls": {
	    "return_url": request.build_absolute_uri(reverse('pedidos.views.paypal_execute')),
	    "cancel_url": "http://localhost:3000/" },

	  # ###Transaction
	  # A transaction defines the contract of a
	  # payment - what is the payment for and who
	  # is fulfilling it.
	  "transactions":  [ {

	    # ### ItemList
	    "item_list": {"items": platos},

	    # ###Amount
	    # Let's you specify a payment amount.
	    "amount":  {
	      "total":  total,
	      "currency":  "EUR" },
	    "description":  "This is the payment transaction description." } ] } )

	# Create Payment and return status
	if payment.create():
		print("Payment[%s] created successfully"%(payment.id))
		request.session['payment_id'] = payment.id
	  	# Redirect the user to given approval url
	  	for link in payment.links:
		    if link.method == "REDIRECT":
		     	redirect_url = link.href
		     	print("Redirect for approval: %s"%(redirect_url))
		     	return HttpResponseRedirect(redirect_url)
	else:
	 	print("Error while creating payment:")
	 	print(payment.error)


def paypal_execute(request):
    payment_id = request.session['payment_id']
    payer_id = request.GET['PayerID']

    paypalrestsdk.configure({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET })

    payment = paypalrestsdk.Payment.find(payment_id)
    payment_name = payment.transactions[0].item_list.items[0].name

    if payment.execute({"payer_id": payer_id}):
        # the payment has been accepted
        print("Payment[%s] execute successfully"%(payment.id))
    	return HttpResponseRedirect(reverse('webapp.views.pago_exitoso'))
    else:
        # the payment is not valid
        print(payment.error)

    return HttpResponseRedirect(reverse('webapp.views.carta'))













def paypal_create2(request):

	paypalrestsdk.configure({
		"mode": PAYPAL_MODE,
		"client_id": PAYPAL_CLIENT_ID,
		"client_secret": PAYPAL_CLIENT_SECRET })
	# ###Payment
	# A Payment Resource; create one using
	# the above types and intent as 'sale'
	payment = paypalrestsdk.Payment({
	  "intent":  "sale",

	  # ###Payer
	  # A resource representing a Payer that funds a payment
	  # Payment Method as 'paypal'
	  "payer":  {
	    "payment_method":  "paypal" },

	  # ###Redirect URLs
	  "redirect_urls": {
	    "return_url": "http://localhost:3000/payment/execute",
	    "cancel_url": "http://localhost:3000/" },

	  # ###Transaction
	  # A transaction defines the contract of a
	  # payment - what is the payment for and who
	  # is fulfilling it.
	  "transactions":  [ {

	    # ### ItemList
	    "item_list": {
	      "items": [{
	        "name": "item",
	        "sku": "item",
	        "price": "5.00",
	        "currency": "USD",
	        "quantity": 1 }]},

	    # ###Amount
	    # Let's you specify a payment amount.
	    "amount":  {
	      "total":  "5.00",
	      "currency":  "USD" },
	    "description":  "This is the payment transaction description." } ] } )

	# Create Payment and return status
	if payment.create():
	  print("Payment[%s] created successfully"%(payment.id))
	  # Redirect the user to given approval url
	  for link in payment.links:
	    if link.method == "REDIRECT":
	      redirect_url = link.href
	      print("Redirect for approval: %s"%(redirect_url))
	      return HttpResponseRedirect(redirect_url)
	else:
	  print("Error while creating payment:")
	  print(payment.error)
