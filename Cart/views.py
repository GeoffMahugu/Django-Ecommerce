import braintree
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

import json
from django.core import serializers
from .models import *

if settings.DEBUG:

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
    )

def AddCart(request):
    if request.is_ajax():
        request.session.set_expiry(0)
        cart_id = request.session.get('cart_id')
    #    cart_id = request.session
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

        if request.user.is_authenticated():
            print(request.user)
            cart.user = request.user
            cart.save()
        else:
            pass

        item_id = request.POST.get('item')
        delete_item = request.POST.get('delete')
        if item_id:
            item_instance = get_object_or_404(Variation, id = item_id)
            qnt = request.POST.get('qnt')
            cart_item = CartItem.objects.get_or_create(cart = cart, item = item_instance)[0]
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qnt
                cart_item.save()
        messages.success(request, 'Cart Item Saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def EditCart(request):
    if request.is_ajax():
        request.session.set_expiry(0)
        cart_id = request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        post = request.POST
        from_client = request.POST['send']
        from_client = json.loads(from_client)  
#        print(from_client)
        for item in from_client:
#            print('item {} => {}'.format(item['id'], item))
            vari_id = int(item['id'])
            vari_obj = get_object_or_404(Variation, pk =vari_id )

            cart_item = CartItem.objects.get_or_create(
                cart= cart, 
                item=vari_obj
            )
            vari_del = item['del']
            if vari_del == 'True':
                cart_item[0].delete()
            else:
                for key, value in item.items():
                    if key == 'id':
                        pass
                    elif key == 'del':
                        pass
                    elif key == 'qnt':
                        cart_item[0].quantity = value
                        cart_item[0].save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def MyCart(request):
    title =  'My Shopping Cart'
    cart_id = request.session.get('cart_id')
    object =  get_object_or_404(Cart, pk=cart_id)
#    print(type(cart))
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
    
    context = {
        'title':title,
        'object':object,
        'cart_count':cart_count,
        'cart_items':cart_items
    }
    return render(request, 'mycart.html',context)

def Checkout(request):
    title = 'Checkout'
    cart_id = request.session.get('cart_id')
    object =  get_object_or_404(Cart, pk=cart_id)
    
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
    uc = UserCheckout.objects.filter(cart =object ) 
    if uc:
        return redirect('/Cart/mycart/checkout/payment/')
    context = {
        'title':title,
        'object':object,
        'cart_count':cart_count,
        'cart_items':cart_items
    }
    return render(request, 'checkout.html',context)

def CheckoutCommit(request):
    cart_id = request.session.get('cart_id')
    object =  get_object_or_404(Cart, pk=cart_id)
    
    if request.method == 'POST':
#        print(request.POST)
#        print(object)
        fname =request.POST.get('firstname') 
        lname =request.POST.get('lastname') 
        email =request.POST.get('email') 
        phone =request.POST.get('phone') 
        add1 =request.POST.get('address1') 
        add2 =request.POST.get('address2') 
        comp =request.POST.get('company') 
        country =request.POST.get('country') 
        state =request.POST.get('state') 
        city =request.POST.get('city') 
        zcode =request.POST.get('zip') 
        user = None
        
        if request.user.is_authenticated():
            user = request.user
        uc = UserCheckout.objects.filter(cart =object )  
        if uc:
            return redirect('/Cart/mycart/checkout/payment/')
        else:
            checkout = UserCheckout.objects.get_or_create(
                user = user,
                cart = object,
                first_name = fname,
                last_name = lname,
                email = email,
                phonenumber = phone,
                address1 = add1,
                address2 = add2,
                company = comp,
                country = country,
                state = state,
                city = city,
                zip_code = zcode
            )
            print(checkout)
            messages.success(request, 'Details Saved')
            return redirect('/Cart/mycart/checkout/payment/')
    return redirect('/Cart/mycart/checkout/payment/')
    
    
    
def Payment(request):
    title = 'Complete Payment'
    cart_id = request.session.get('cart_id')
    object =  get_object_or_404(Cart, pk=cart_id)
    amount = object.total
    cart_count = object.cartitem_set.count()
    cart_items = object.cartitem_set.all()
#    checkout_obj =get_object_or_404(UserCheckout, cart=object) 
    checkout_obj = UserCheckout.objects.get(cart=object) 
#    print(checkout_obj.braintree_id)
    client_token = checkout_obj.get_client_token()
#    print(client_token)
    context = {
        'title':title,
        'cart_count':cart_count,
        'cart_items':cart_items,
        'checkout_obj':checkout_obj,
        'object':object,
        'client_token':client_token

    }
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')
        if nonce:
            result = braintree.Transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "customer": {

                "company": checkout_obj.company,
                "email": checkout_obj.email,
                "phone": checkout_obj.phonenumber,
#                'country_name':checkout_obj.country,
#                'postal_code':checkout_obj.zip_code,
                "first_name": checkout_obj.first_name,
                "last_name": checkout_obj.last_name,
              },
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            del request.session["cart_id"]
            checkout_obj.status = 'Completed'
            checkout_obj.save()
#                del request.session["order_id"]
            messages.success(request,'Your Payment Been Successfully Completed')
            return redirect('/Products/home/')

        else:
            checkout_obj.status = 'Pending'
            checkout_obj.save()
            messages.success(request,'%s' %(result.message))
            return redirect('/Products/home/')
#            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'payment.html',context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    