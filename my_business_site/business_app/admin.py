from django.contrib import admin
from .models import Product
from .models import Catalog
from .models import Arrival
from .models import Staff
from .models import Client
from .models import Sale
from .models import Transfer
from .models import ArrivalProduct
from .models import SaleProduct
from .models import TransferProduct
from .models import Shipment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'catalog', 'manufacturer', 'country_of_origin', 'quantity_in_stock')
    list_filter = ('catalog', 'manufacturer', 'country_of_origin')
    search_fields = ('name', 'manufacturer')

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog_name',)
    search_fields = ('catalog_name',)

@admin.register(Arrival)
class ArrivalAdmin(admin.ModelAdmin):
    list_display = ('date_of_arrival', 'city_of_departure', 'vehicle_number', 'driver_name', 'total_weight')
    list_filter = ('date_of_arrival', 'city_of_departure')
    search_fields = ('vehicle_number', 'driver_name')

@admin.register(ArrivalProduct)
class ArrivalProductAdmin(admin.ModelAdmin):
    list_display = ('arrival', 'product', 'quantity')
    list_filter = ('arrival', 'product')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position')
    list_filter = ('position',)
    search_fields = ('full_name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'ownership_type', 'contract_number', 'registration_date', 'payment_method')
    list_filter = ('ownership_type', 'payment_method')
    search_fields = ('company_name', 'contract_number')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'buyer', 'seller', 'invoice_number', 'bill_of_lading_number', 'total_amount_with_vat')
    list_filter = ('sale_date', 'buyer', 'seller')
    search_fields = ('invoice_number', 'bill_of_lading_number')

@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('sale', 'shipment', 'product', 'quantity')
    list_filter = ('sale', 'shipment', 'product')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_date', 'city_of_receipt', 'vehicle_number', 'driver_name', 'total_weight')
    list_filter = ('transfer_date', 'city_of_receipt')
    search_fields = ('vehicle_number', 'driver_name')

@admin.register(TransferProduct)
class TransferProductAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'product', 'quantity')
    list_filter = ('transfer', 'product')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('sale', 'shipment_date', 'status')
    list_filter = ('shipment_date', 'status')
    search_fields = ('sale__invoice_number', 'sale__bill_of_lading_number')

# @admin.register(ShipmentItem)
# class ShipmentItemAdmin(admin.ModelAdmin):
#     list_display = ('shipment', 'product', 'quantity')
#     list_filter = ('shipment__shipment_date',)
