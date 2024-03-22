from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords


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
        return f"{self.buyer} | накл.№{self.bill_of_lading_number}"


class Shipment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='shipments')
    next_shipment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='previous_shipment')
    shipment_date = models.DateField(verbose_name='Дата отгрузки')
    STATUS_CHOICES = [
        ('shipped', 'Отгружено'),
        ('not_shipped', 'Не отгружено'),
        ('postponed', 'Перенесено')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    history = HistoricalRecords()

    def __str__(self):
        return f"Отгрузка для {self.sale} от {self.shipment_date}"

class SaleProduct(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_products')
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='shipment_items', null=True,
                                 blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def clean(self):
        # Проверяем, достаточно ли товара на складе
        if self.product.quantity_in_stock < self.quantity:
            raise ValidationError(f"На складе недостаточно товара для продажи. Доступное количество: {self.product.quantity_in_stock}.")

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

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

    def clean(self):
        # Проверяем, достаточно ли товара на складе
        if self.product.quantity_in_stock < self.quantity:
            raise ValidationError(f"На складе недостаточно товара для перемещения. Доступное количество: {self.product.quantity_in_stock}.")

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

