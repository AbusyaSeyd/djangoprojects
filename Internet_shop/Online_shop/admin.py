from django.contrib import admin

from Online_shop.models import Category
from Online_shop.models import *

admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(Product)



class ProductAdmin(admin.ModelAdmin):
	"""docstring for ProductAdmin"""
	list_display=('title','brand','price','available')
	list_filter=['available']

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)

admin.site.register(CartItem)
class OrderView(admin.ModelAdmin):


	list_display=('id','first_name','last_name','phone',)
	list_filter=['buying_type','status','date']

admin.site.register(Order,OrderView)
# Register your models here.
