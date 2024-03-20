from django.contrib import admin
from .models import StockEntry
from .models import Sale
from .models import Product
from .models import Reservation
from .models import Customer


admin.site.register(Product)
admin.site.register(StockEntry)
admin.site.register(Sale)
admin.site.register(Reservation)
admin.site.register(Customer)
