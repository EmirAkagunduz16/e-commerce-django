from django.contrib import admin

# Register your models here.

from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
    readonly_fields = ['order_number', 'payment', 'user', 'created_at', 'updated_at']
    fieldsets = (
        ('Order Information', {'fields': ('order_number', 'payment', 'user', 'created_at', 'updated_at')}),
        ('Shipping Information', {'fields': ('first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'city', 'order_note')}),
    )
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return True
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
 
        
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'amount_paid', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user', 'payment_id']
    list_per_page = 20
    readonly_fields = ['user', 'payment_id', 'amount_paid', 'status', 'created_at']
    fieldsets = (
        ('Payment Information', {'fields': ('user', 'payment_id', 'amount_paid', 'status', 'created_at')}),
    )

    

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderProduct)