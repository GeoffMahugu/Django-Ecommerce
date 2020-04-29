from django.conf.urls import url

from .views import *
urlpatterns = [
    url(r'^add/$', AddCart, name='AddCart'),
    url(r'^mycart/$', MyCart, name='MyCart'),
    url(r'^mycart/edit/$', EditCart, name='EditCart'),
    url(r'^mycart/checkout/$', Checkout, name='Checkout'),
    url(r'^mycart/checkout/commit/$', CheckoutCommit, name='CheckoutCommit'),
    url(r'^mycart/checkout/payment/$', Payment, name='Payment'),
]
