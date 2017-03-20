from django import forms
from django.forms.models import modelformset_factory
from .models import Product,Variation, Category,ProductFeatured

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields  = [
            'title',
            'categories',
            'default_category',
            'description',
            'price',
            'default_image',
            'active',
        ]
        
class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields  = [
            'product',
            'title',
            'price',
            'sale_price',
            'color',
            'inventory',
            'image',
            'active',
            'currency'
        ]
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields  = [
            'title',
            'description',
            'active',
        ]
        exclude = [
            'slug',
        ]
        
class ProductFeaturedForm(forms.ModelForm):
    class Meta:
        model = ProductFeatured
        fields  = [
            'product',
            'title',
            'text',
            'active',
        ]


