from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Create your models here.


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        products_one = self.get_queryset().filter(
            categories__in=instance.categories.all())
        products_two = self.get_queryset().filter(default=instance.default)
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs


def image_upload_to_prod(instance, filename):
    title = instance.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s.%s" % (slug, file_extension)
    return "products/%s" % (slug)


class Product(models.Model):
    title = models.CharField(max_length=120)
    categories = models.ManyToManyField('Category', blank=True)
    SKU = models.CharField(max_length=120, blank=True, null=True)
    default_category = models.ForeignKey(
        'Category', related_name='default_category', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    default_image = models.ImageField(
        upload_to=image_upload_to_prod, blank=True, null=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    objects = ProductManager()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Products:SingleProduct', kwargs={'pk': self.pk})


def upload_location(objects, filename):
    title = objects.product.title
    slug = slugify(title)
    return "Products/%s" % (slug)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True)
    DEFAULT = 'DEFAULT'
    RED = 'RED'
    BLUE = 'BLUE'
    YELLOW = 'YELLOW'
    ORANGE = 'ORANGE'
    GREEN = 'GREEN'
    PINK = 'PINK'
    BLACK = 'BLACK'
    WHITE = 'WHITE'
    GREY = 'GREY'
    TYP = (
        (DEFAULT, 'DEFAULT'),
        (RED, 'RED'),
        (BLUE, 'BLUE'),
        (YELLOW, 'YELLOW'),
        (ORANGE, 'ORANGE'),
        (GREEN, 'GREEN'),
        (PINK, 'PINK'),
        (BLACK, 'BLACK'),
        (WHITE, 'WHITE'),
        (GREY, 'GREY')
    )
    color = models.CharField(max_length=100, choices=TYP, default=DEFAULT)
    NA = 'N/A'
    UNISEX = 'Unisex'
    MALE = 'Male'
    FEMALE = 'N/A'
    FEMALE = 'Female'
    TYP = (
        (NA, 'N/A'),
        (UNISEX, 'Unisex'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    gender = models.CharField(max_length=100, choices=TYP, default=UNISEX)
    NA = 'N/A'
    CHILDREN = 'Children'
    ADULT = 'Adult'
    TYP = (
        (NA, 'N/A'),
        (CHILDREN, 'Children'),
        (ADULT, 'Adult')
    )
    age = models.CharField(max_length=100, choices=TYP, default=NA)
    currency = models.CharField(
        max_length=120, null=True, blank=True, default='Ksh')
    inventory = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_image(self):
        if self.image is not None:
            return self.product.default_image
        else:
            return self.image

    def get_absolute_url(self):
        return self.product.get_absolute_url()


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.sale_price = product.price
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Products:SingleCategory', kwargs={'slug': self.slug})


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    title = instance.title
    slug = slugify(title)
    instance.slug = slug


pre_save.connect(category_pre_save_receiver, sender=Category)


class ProductFeatured(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=220, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField()
    FIVE = '5'
    FOUR = '4'
    THREE = '3'
    TWO = '2'
    ONE = '3'
    NUM = (
        (FIVE, '5'),
        (FOUR, '4'),
        (THREE, '3'),
        (TWO, '2'),
        (ONE, '1')
    )
    stars = models.CharField(max_length=100, choices=NUM, default=FIVE)
    caption = models.CharField(max_length=120, null=True, blank=True)
    review = models.TextField()
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name
