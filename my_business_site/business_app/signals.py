from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ArrivalProduct, TransferProduct, SaleProduct


@receiver(post_save, sender=ArrivalProduct)
def update_product_quantity(sender, instance, **kwargs):
    """
    Обновляет количество товара на складе при добавлении товара через ArrivalProduct.
    """
    product = instance.product
    product.quantity_in_stock += instance.quantity
    product.save()

@receiver(post_save, sender=TransferProduct)
def update_stock_on_transfer(sender, instance, **kwargs):
    """
    Уменьшает количество товара на складе при создании объекта TransferProduct.
    """
    product = instance.product
    product.quantity_in_stock -= instance.quantity
    product.save()

@receiver(post_save, sender=SaleProduct)
def update_stock_on_sale(sender, instance, **kwargs):
    """
    Уменьшает количество товара на складе при продаже.
    """
    product = instance.product
    product.quantity_in_stock -= instance.quantity
    product.save()