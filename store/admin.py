from django.db.models import Count
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
            'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        #return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Order)
class OrderAmdin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    #list_select_related = ['customer']
    list_per_page = 10

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist') 
            + '?' 
            + urlencode({'order_id': str(order.id)})
        )
        return format_html('<a href="{}">{}</a>', url, order.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

   