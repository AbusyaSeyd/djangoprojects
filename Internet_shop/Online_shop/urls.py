
from django.urls import path, include
from .models import *


# from Online_shop.views import sign, base_view, category_view, product_view
# from Online_shop.views import world
# from Online_shop.views import categories
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from Online_shop.views import *
# from Online_shop.views import  example_view


urlpatterns = [
    
	path('',base_view, name = 'base_view'),
    
    path('categories/',categories, name = 'categories'),
    path('sign/',sign),

    ####################################
    path('category/<category_slug>', category_view, name='category_details'),
    path('product/<product_slug>', product_view, name='product_details'),

    # path('add_to_cart_view/(?P<product_slug>[-\w]+)/$', add_to_cart_view, name='add_to_cart'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/',remove_from_cart_view, name='remove_from_cart'),

    path('change_item_qty/', change_item_qty, name='change_item_qty'),

    

    path('cart/', cart_view,name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    # url(r'^checkout/$', checkout_view, name='checkout'),
    path('order/', order_create_view, name='create_order'),
    path('make_order/', make_order_view, name='make_order'),
    path('thank_you/', thank_you, name='thank_you'),




    path('account/', account_view, name='account'),
    
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base_view')), name='logout'),



    path('world',world),
    # path('example_view',example_view, name = 'example_view'),
]
