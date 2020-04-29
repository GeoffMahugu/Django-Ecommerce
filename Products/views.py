from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Count
import json
from django.core import serializers
import random

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import*
from Cart.models import *
from .forms import*


def Home(request):
    request.session.set_expiry(0)
    title = 'Welcome to E-Shop Kenya'
    products = Product.objects.all().order_by('?')
    featured = Product.objects.filter(featured=True).order_by('?')[:4]
    categories = Category.objects.all()
    prod_no = products.count()
    cart_id = request.session.get('cart_id')
    if cart_id == None:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
    cart = Cart.objects.get(pk=cart_id)
    cart_count = cart.cartitem_set.count()
    cart_items = cart.cartitem_set.all()
    context = {
        'title': title,
        'products': products,
        'featured': featured,
        'categories': categories,
        'prod_no': prod_no,
        'cart': cart,
        'cart_count': cart_count,
        'cart_items': cart_items

    }
    return render(request, 'base.html', context)


def AddProduct(request):
    title = 'Add Product'
    form = ProductForm(request.POST or None, request.FILES or None)
    context = {
        'title': title,
        'form': form
    }
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Product Saved')
            return redirect('Products:AddProduct')
        else:
            messages.error(request, " Unsuccessfuly Adding Product")
    else:
        return render(request, 'baseform.html', context)


def AddVariation(request):
    title = 'Add Product Variation'
    form = VariationForm(request.POST or None, request.FILES or None)
    context = {
        'title': title,
        'form': form
    }
    if request.method == 'POST':
        form = VariationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Variation Saved')
            return redirect('Products:AddVariation')
        else:
            messages.error(request, " Unsuccessfuly Adding Variation")
    else:
        return render(request, 'baseform.html', context)


def AddCategory(request):
    title = 'Add Product Category'
    form = CategoryForm(request.POST or None)
    context = {
        'title': title,
        'form': form
    }
    if request.method == 'POST':
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Category Saved')
            return redirect('Products:AddCategory')
        else:
            messages.error(request, " Unsuccessfuly Adding Category")
    else:
        return render(request, 'baseform.html', context)


@login_required(login_url='../../login/')
def AddFeatured(request):
    title = 'Add Featured Product '
    form = ProductFeaturedForm(request.POST or None)
    context = {
        'title': title,
        'form': form
    }
    if request.method == 'POST':
        form = ProductFeaturedForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Featured Product Saved')
            return redirect('Products:AddFeatured')
        else:
            messages.error(request, " Unsuccessfuly Adding Featured Product")
    else:
        return render(request, 'baseform.html', context)


@login_required(login_url='../../login/')
def AddUser(request):
    title = 'Login and Register '
    cart_id = request.session.get('cart_id')
    context = {
        'title': title
    }

    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:

            user = User.objects.create(
                username=uname,
                email=email,
                password=pass1
            )
            if cart_id == None:
                cart = Cart()
                cart.user = user
                cart.save()
                cart_id = cart.id
                request.session['cart_id'] = cart_id
            cart = Cart.objects.get(pk=cart_id)
            cart.user = user
            cart.save()

            messages.success(request, 'Featured Product Saved')
            return redirect('Products:Home')
    else:
        return render(request, 'adduser.html', context)


def CartShortcutUpdate(request):
    cart_id = request.session.get('cart_id')
    object = get_object_or_404(Cart, pk=cart_id)
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
    data = serializers.serialize("json", cart_items)
    return HttpResponse(data, content_type='application/json')


def SingleProduct(request, pk=None):
    objects = get_object_or_404(Product, pk=pk)
    vari = Variation.objects.filter(product=objects)
    reviews = Review.objects.filter(
        product=objects).filter(active=True).order_by('-pk')
    obj_cat = objects.default_category
    obj_prod = Product.objects.filter(default_category=obj_cat).exclude(
        pk=objects.pk).order_by('-pk')[:3]
    rev_count = reviews.count()
    title = '%s' % (objects.title)

    cart_id = request.session.get('cart_id')
    object = get_object_or_404(Cart, pk=cart_id)
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()

    context = {
        'vari': vari,
        'reviews': reviews,
        'rev_count': rev_count,
        'title': title,
        'objects': objects,
        'obj_prod': obj_prod,
        'cart_count': cart_count,
        'cart_items': cart_items
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        stars = request.POST.get('stars')
        caption = request.POST.get('caption')
        review = request.POST.get('review')

        try:
            r_object = Review.objects.get_or_create(
                product=objects,
                name=name,
                email=email,
                stars=stars,
                caption=caption,
                review=review
            )
            print(r_object[1])
            status = r_object[1]
            if status == 'True':
                messages.success(request, 'Review Saved')
            else:
                pass
        except:
            pass
        messages.success(request, 'Porduct Added to cart')
    else:
        return render(request, 'svariable.html', context)
    return render(request, 'svariable.html', context)


def SingleCategory(request, slug=None):
    object = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(categories=object)
    categories = Category.objects.all()
    prod_no = products.count()
    title = '%s' % (object.title)
    context = {
        'title': title,
        'object': object,
        'products': products,
        'categories': categories,
        'prod_no': prod_no
    }
    return render(request, 'base.html', context)
