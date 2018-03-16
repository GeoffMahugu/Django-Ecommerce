from django.conf.urls import url

from .views import *
urlpatterns = [
    url(r'^home/$',Home, name = 'Home'),
    url(r'^addproduct/$',AddProduct, name = 'AddProduct'),
    url(r'^addvariation/$',AddVariation, name = 'AddVariation'),
    url(r'^addcategory/$',AddCategory, name = 'AddCategory'),
    url(r'^addfeatured/$',AddFeatured, name = 'AddFeatured'),
    url(r'^home/adduser/$',AddUser, name = 'AddUser'),
    url(r'^supdate/$', CartShortcutUpdate, name = 'CartShortcutUpdate'),
    
    url(r'^home/(?P<pk>\d+)/$', SingleProduct , name='SingleProduct'),
    url(r'^(?P<slug>[\w-]+)/$', SingleCategory, name='SingleCategory'),
]