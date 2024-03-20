from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField()

    def __str__(self):
        return self.name

class StockEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units of {self.product.name}"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_sales')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_sales')

    def __str__(self):
        return f"{self.quantity_sold} units of {self.product.name} sold by {self.manager.username}"

class Reservation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_reserved = models.IntegerField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity_reserved} units of {self.product.name} reserved"

