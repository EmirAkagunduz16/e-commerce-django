from django.contrib import admin
from .models import Product, Variation, ReviewRating


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('category', 'is_available')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_filter = ('product', 'variation_category', 'variation_value')
    list_editable = ('is_active',)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status')
    list_filter = ('product', 'user', 'subject', 'rating', 'status')
    list_editable = ('status',)
    search_fields = ('product', 'user', 'subject', 'rating', 'status')
    list_per_page = 10
    

admin.site.register(Product, ProductAdmin)  
admin.site.register(Variation, VariationAdmin)  
admin.site.register(ReviewRating, ReviewRatingAdmin)