from django.db import models

class Catalog(models.Model):
    catalog_name = models.CharField(max_length=255)

    def __str__(self):
        return self.catalog_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField(default=0)  # Добавлено для учета количества на складе

    def __str__(self):
        return self.name

class Arrival(models.Model):
    date_of_arrival = models.DateField()
    city_of_departure = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    total_weight = models.IntegerField()

    def __str__(self):
        # Возвращает дату прихода как строковое представление объекта Arrival
        return self.date_of_arrival.strftime('%d-%m-%Y')

class ArrivalProduct(models.Model):
    arrival = models.ForeignKey(Arrival, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    POSITION_CHOICES = [
        ('storekeeper', 'Кладовщик'),
        ('manager', 'Менеджер'),
        ('chief', 'Начальник')
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    def __str__(self):
        return self.full_name

class Client(models.Model):
    company_name = models.CharField(max_length=255)
    OWNERSHIP_CHOICES = [
        ('LLC', 'ТОВ'),
        ('FOP', 'ФОП'),
        ('PP', 'ПП'),
        ('individual', 'Физическое лицо')
        # Добавьте другие формы собственности по необходимости
    ]
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_CHOICES)
    contract_number = models.CharField(max_length=255)
    registration_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[('prepayment', 'Предоплата'), ('deferment', 'Отсрочка')])
    payment_delay_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.company_name

class Sale(models.Model):
    sale_date = models.DateField()
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE)
    seller = models.ForeignKey(Staff, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=255)
    bill_of_lading_number = models.CharField(max_length=255)
    total_amount_with_vat = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bill_of_lading_number} to {self.buyer}"

class SaleProduct(models.Model):  # Эта модель связывает продажи с товарами
    sale = models.ForeignKey(Sale, related_name='sale_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in sale {self.sale.invoice_number}"

class Transfer(models.Model):
    transfer_date = models.DateField()
    city_of_receipt = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255)
    total_weight = models.IntegerField()

    def __str__(self):
        # Возвращает дату прихода как строковое представление объекта Arrival
        return self.transfer_date.strftime('%d-%m-%Y')

class TransferProduct(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
