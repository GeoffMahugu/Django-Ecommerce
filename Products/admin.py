from django.contrib import admin
from .models import Product, Variation, Category, ProductFeatured,Review



class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0
	max_num = 10


class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price']
	inlines = [
		VariationInline,
	]
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Variation)
admin.site.register(ProductFeatured)
admin.site.register(Review)