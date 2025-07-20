from django.contrib import admin
from .models import ServiceCategory, Service, PriceTable, Order

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'category', 'is_popular']
    list_filter = ['category', 'is_popular']
    search_fields = ['name']

@admin.register(PriceTable)
class PriceTableAdmin(admin.ModelAdmin):
    list_display = ['service', 'unit', 'price']
    list_filter = ['service']
    search_fields = ['service__name', 'unit']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'service', 'unit', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'service']
    search_fields = ['customer_name', 'phone', 'id']
    list_editable = ['status']
    readonly_fields = ['created_at', 'total_price']