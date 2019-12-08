from django.db import models
from django.db import __str__
from django.forms import ModelForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
################
from django.db.models.signals import pre_save
from django.utils.text import slugify
###########
from transliterate import translit
from django.utils.translation import gettext
##########
from django.urls import reverse
# ##################
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.

class Category(models.Model):

	name = models.CharField(max_length=100)
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category_details', kwargs={'category_slug': self.slug})


###### slug tranlit
def pre_save_category_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug = slugify(translit(gettext(instance.name),reversed=True))

		instance.slug = slug

pre_save.connect(pre_save_category_slug, sender=Category)



class Brand(models.Model):
	name = models.CharField(max_length=100)
	
	"""docstring for  Brand"""
	def __str__(self):
		return self.name



def images_folder(instance, filename):
	filename = instance.slug+ '.' + filename.split('.')[1]
	return "{0}/{1}".format(instance.slug, filename)



class ProductManager(models.Manager):
	"""docstring for ProductManager"""
	def all(self, *args, **kwargs):
		return super(ProductManager, self).get_queryset().filter(available=True)
		



class Product(models.Model):

	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
	title = models.CharField(max_length=120) # Название товара
	
	slug = models.SlugField() 
	description = models.TextField() # Описание
	image = models.ImageField(upload_to=images_folder) # image
	price = models.DecimalField(max_digits=9, decimal_places=2) # max_digits=9 сколько цифр-place, decimal_places=2 --> 999.33
	available = models.BooleanField(default=True)
	objects = ProductManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product_details', kwargs={'product_slug': self.slug})

class CartItem(models.Model):
	"""docstring for CartItem"""
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	qty = models.PositiveIntegerField(default=1)
	item_total = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)

	def __str__(self):
		return "Cart item for product {0}".format(self.product.title)

	def get_absolute_url(self):
		return reverse('product_details', kwargs={'product_slug': self.slug})

class Cart(models.Model):
	
	items = models.ManyToManyField(CartItem, blank=True)
	cart_total = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)


	
	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('product_details', kwargs={'product_slug': self.slug})


	def add_to_cart(self,product_slug):
		cart = self
		product = Product.objects.get(slug=product_slug)
		new_item, _ =CartItem.objects.get_or_create(product=product,item_total=product.price)
		# cart = Cart.objects.first()

		if new_item  in cart.items.all():
			
			return HttpResponseRedirect('Этот товаr имеется')


		if new_item not in cart.items.all():
			cart.items.add(new_item)
			cart.save()
			return HttpResponseRedirect('/cart/')

	def remove_from_cart(self,product_slug):
		cart = self
		product = Product.objects.get(slug=product_slug)

		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()
				return HttpResponseRedirect('/cart/')





ORDER_STATUS_CHOICES = (
	('Принят в обработку', 'Принят в обработку'),
	('Выполняется', 'Выполняется'),
	('Оплачен', 'Оплачен')
)

class Order(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	items = models.ForeignKey(Cart, on_delete = models.CASCADE)
	total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=255)
	buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), 
		('Доставка', 'Доставка')), default='Самовывоз')
	date = models.DateTimeField(auto_now_add=True)
	comments = models.TextField()
	status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

	def __str__(self):
		return "Заказ №{0}".format(str(self.id))








	# __repr__ = __str__

	# def __repr__(self):
	# 	return self.__str__(self.id)