import braintree
from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from Products.models import Variation

if settings.DEBUG:

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
    )

class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete = models.CASCADE)
    item = models.ForeignKey(Variation, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title

#	def remove(self):
#		return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) >= 1:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total
pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()
    
post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    currency = models.CharField(max_length = 50, default = 'Ksh')
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    #	tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
    #	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
	# discounts
	# shipping

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        print("updating...")
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
            self.subtotal = "%.2f" %(subtotal)
            self.total = "%.2f" %(subtotal)
            self.save()
            

        

#def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
#	subtotal = Decimal(instance.subtotal)
#	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
#	print instance.tax_percentage
#	total = round(subtotal + Decimal(tax_total), 2)
#	instance.tax_total = "%.2f" %(tax_total)
#	instance.total = "%.2f" %(total)
#	#instance.save()
#
#pre_save.connect(do_tax_and_total_receiver, sender=Cart)

#STATUS = (
#    ('completed','Completed'),
#    ('pending','Pending')
#)

class UserCheckout(models.Model):
    Completed = 'Completed'
    Pending = 'Pending'
    Status = (
        (Completed, 'Completed'),
        (Pending, 'Pending')
    )
    stars = models.CharField(max_length = 100, choices=Status, default = Pending)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    cart = models.OneToOneField(Cart,unique = True, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    email = models.EmailField()
    phonenumber = models.CharField(max_length = 250)
    address1 = models.CharField(max_length = 250)
    address2 = models.CharField(max_length = 250)
    company = models.CharField(max_length = 250)
    country = models.CharField(max_length = 250)
    state = models.CharField(max_length = 250)
    city = models.CharField(max_length = 250)
    zip_code = models.CharField(max_length = 250)
    braintree_id = models.CharField(max_length= 300, null=True, blank=True)
    def __str__(self):
        return self.first_name+' '+self.last_name
    
    @property
    def get_braintree_id(self):
        instance = self
        if not instance.braintree_id:
            result = braintree.Customer.create({
                "company": instance.company,
                "email": instance.email,
                "phone": instance.phonenumber,
#                'country_name':instance.country,
#                'postal_code':instance.zip_code,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id
                
    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            
            client_token = braintree.ClientToken.generate({
                'customer_id':customer_id
            })
            return client_token
        return None
    
def update_braintree_id(sender, instance, *args, **kwargs):
    if not instance.braintree_id:
        instance.get_braintree_id
post_save.connect(update_braintree_id, sender=UserCheckout)







