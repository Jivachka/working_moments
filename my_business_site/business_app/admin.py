from django.contrib import admin
from .models import Product, Catalog, Arrival, Staff, Client, Sale, Transfer, ArrivalProduct, SaleProduct, TransferProduct

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'catalog', 'manufacturer', 'country_of_origin', 'quantity_in_stock')
    list_filter = ('catalog', 'manufacturer', 'country_of_origin')
    search_fields = ('name', 'manufacturer')

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog_name',)
    search_fields = ('catalog_name',)

class ArrivalAdmin(admin.ModelAdmin):
    list_display = ('date_of_arrival', 'city_of_departure', 'vehicle_number', 'driver_name', 'total_weight')
    list_filter = ('date_of_arrival', 'city_of_departure')
    search_fields = ('vehicle_number', 'driver_name')

class ArrivalProductAdmin(admin.ModelAdmin):
    list_display = ('arrival', 'product', 'quantity')
    list_filter = ('arrival', 'product')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position')
    list_filter = ('position',)
    search_fields = ('full_name',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'ownership_type', 'contract_number', 'registration_date', 'payment_method')
    list_filter = ('ownership_type', 'payment_method')
    search_fields = ('company_name', 'contract_number')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'buyer', 'seller', 'invoice_number', 'bill_of_lading_number', 'total_amount_with_vat')
    list_filter = ('sale_date', 'buyer', 'seller')
    search_fields = ('invoice_number', 'bill_of_lading_number')

class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('sale', 'sale_date', 'product', 'quantity')
    list_filter = ('sale', 'product', 'sale_date', )

class TransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_date', 'city_of_receipt', 'vehicle_number', 'driver_name', 'total_weight')
    list_filter = ('transfer_date', 'city_of_receipt')
    search_fields = ('vehicle_number', 'driver_name')

class TransferProductAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'product', 'quantity')
    list_filter = ('transfer', 'product')

# Регистрация моделей с классами ModelAdmin
admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Arrival, ArrivalAdmin)
admin.site.register(ArrivalProduct, ArrivalProductAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(TransferProduct, TransferProductAdmin)
