from .forms import OpinionForm
from .models import Detalle_pedido, Opinion, Pedido
import paypalrestsdk
from carton.cart import Cart
from clientes.models import Cliente
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from restaurante.models import Plato, Restaurante
from django.template import RequestContext
from UFood.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
from django.views.generic.edit import CreateView


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
	plato = Plato.objects.get(id=request.GET.get('product_id'))
	cart.remove_single(plato)
	return platilla_cesta(request);

def clear(request):
	cart = Cart(request.session)
	pass

def set_queantity(request):
	cart = Cart(request.session)
	pass


@login_required
def pago(request):
	if request.method == "POST":
		cart = Cart(request.session)
		if not cart.is_empty:
			#
			#	Guardo el pedido
			# ===========================
			
			# creo un pedido con los datos del cliente y el restaurante
			restaurante =cart.items[0].product.restaurante
			cliente = Cliente.objects.get(user=request.user) #falta el cliente
			pedido = Pedido (restaurante=restaurante, cliente=cliente)
			pedido.save()
			
			#aado platos al pedido
			for item in cart.items:
				plato = item.product
				Detalle_pedido(plato=plato, pedido=pedido, cantidad=item.quantity).save()
						
			

			if request.POST.get('pago') == "Paypal":
				return paypal_create(request)
			elif request.POST.get('pago') == "Efectivo":
				cart.clear() #Se vacia el carrito
				return HttpResponseRedirect(reverse('pago_exitoso'))



	

@login_required
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
	    "return_url": request.build_absolute_uri(reverse('paypal_execute')),
	    "cancel_url": request.build_absolute_uri(reverse('detalles_pedido'))
	   },

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


@login_required()
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
        Cart(request.session).clear()
        print("Payment[%s] execute successfully"%(payment.id))
    	return HttpResponseRedirect(reverse('pago_exitoso'))
    else:
        # the payment is not valid
        print(payment.error)

    return HttpResponseRedirect(reverse('home'))







@login_required(redirect_field_name='/detalles-pedido/')
def detalles_pedido(request):
	cart = Cart(request.session)
	platos = []
	for item in cart.items:
		 platos.append(item.product)
	cliente = Cliente.objects.get(user=request.user)
	pedido = {'cliente': cliente, 'items': cart.items, 'total': cart.total}
	return render_to_response('pedidos/detalles_pedido.html', pedido, context_instance=RequestContext(request))




class OpinionCreateView(CreateView):
    model = Opinion
    context_object_name = "opinion"
    template_name = "pedidos/opinion.html"
    success_url = '/'
    form_class = OpinionForm

    def post(self, request, *args, **kwargs):
    	self.object = None
    	form_class = self.get_form_class()
    	form = self.get_form(form_class)
    	if form.is_valid():
    		print form.cleaned_data['valoracion']
    		return self.form_valid(form)
    	else:
    		return self.form_invalid(form)

    def form_valid(self, form):
        opinion = self.object = form.save(commit=False)
        opinion.pedido = Pedido.objects.get(id=self.kwargs['id_pedido'])
        opinion.save()
        return HttpResponseRedirect(self.get_success_url())
