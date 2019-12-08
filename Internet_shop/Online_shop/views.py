from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse, Http404
from django.urls import reverse
# from Online_shop.models import Category


# from django.template import loader
from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from Online_shop.forms import *
from .models import *

from django.contrib.auth import login, authenticate

from django.views.generic import View
from django.contrib.auth.models import User





def base_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	
	categories = Category.objects.all()
	products = Product.objects.all()

	context = {
	'cart': cart,
	'categories': categories,
	'products': products,

	}

	return render(request,'Online_shop/main.html', context)

def product_view(request, product_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	# product_slug = request.GET.get('product_slug')
	product = Product.objects.get(slug=product_slug)
	categories = Category.objects.all()
	context= {
	'cart': cart,
	'product': product,
	'categories': categories,
	}

	return render(request, 'Online_shop/product.html', context)


def category_view(request, category_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	category = Category.objects.get(slug=category_slug)
	products_of_categoty= Product.objects.filter(category=category)
	context= {
	'cart': cart,
	'category': category,
	'products_of_categoty': products_of_categoty,
	}

	return render(request, 'Online_shop/category.html', context)

def cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	# product = Product.objects.get(slug=product_slug)

	context= {
	# 'category': category,
	'cart': cart,
	# 'product': product,
	}

	return render(request, 'Online_shop/cart.html', context)

def add_to_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	product_slug = request.GET.get('product_slug')
	product = Product.objects.get(slug=product_slug)
	cart.add_to_cart(product.slug)

	# ИТОГОВЫЙ ЦЕНА
	new_cart_total =0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()

	return JsonResponse({'cart_total': cart.items.count(),'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)


	product_slug = request.GET.get('product_slug')
	product = Product.objects.get(slug=product_slug)
	cart.remove_from_cart(product.slug)

	# ИТОГОВЫЙ ЦЕНА
	new_cart_total =0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()

	 
	return JsonResponse({'cart_total': cart.items.count(),'cart_total_price': cart.cart_total})

def change_item_qty(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	qty = request.GET.get('qty')
	item_id = request.GET.get('item_id')
	# print(qty, item_id)
	cart_item = CartItem.objects.get(id=int(item_id))
	cart_item.qty = int(qty)
	cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
	cart_item.save()

	# ИТОГОВЫЙ ЦЕНА
	new_cart_total =0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()

	return JsonResponse(
		{'cart_total': cart.items.count(),
		'item_total': cart_item.item_total,
		'cart_total_price': cart.cart_total
		}) 

def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
		'cart': cart,
		'categories': categories,
	}

	return render(request, 'Online_shop/checkout.html', context)
	

def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)


	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	context = {
		'form': form,
		'cart': cart,
		'categories': categories
	}
	return render(request, 'Online_shop/order.html', context)

def thank_you(request):
	return render(request,'Online_shop/thank_you.html',{})

	

def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	
	if form.is_valid():
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		address = form.cleaned_data['address']
		comments = form.cleaned_data['comments']
		
		# new_order = Order()
		# new_order.user = request.user
		# new_order.save()
		# new_order.items.add(cart)
		# new_order.first_name=name
		# new_order.last_name=last_name
		# new_order.phone = phone
		# new_order.address=address
		# new_order.buying_type=buying_type
		# new_order.comments=comments
		# new_order.total=cart.cart_total

		# new_order.save()


		new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.cart_total,
			first_name=name,
			last_name=last_name,
			phone=phone,
			address=address,
			buying_type=buying_type,
			comments=comments
			)
		del request.session['cart_id']
		# del request.session['total']
		request.session['total'] = cart.items.count()
		return HttpResponseRedirect(reverse('thank_you'))
	return render(request, 'Online_shop/order.html', {'categories': categories})
		
def account_view(request):
	order = Order.objects.filter(user=request.user).order_by('-id')
	categories = Category.objects.all()
	for item in order:
		for new_item in item.items.items.all():
			print(new_item.item_total)
	context = {
		'order': order,
		'categories': categories
	}
	return render(request, 'Online_shop/account.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']

		new_user.username = username
		new_user.set_password(password)
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.email = email
		new_user.save()

		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base_view'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'Online_shop/registration.html', context)


def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base_view'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'Online_shop/login.html', context)



def sign(request):
  	return render(request,'Online_shop/base.html',{})

def world(request):
	return render(request,'Online_shop/pages/index.html')

def categories(request):
	return render(request,'Online_shop/pages/categories.html')



# def example_view(request):
# 	return render(request, 'Online_shop/pages/categories.html')




# Create your views here.
