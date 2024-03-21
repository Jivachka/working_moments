from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import ArrivalProduct, TransferProduct, SaleProduct

# Словарь для временного хранения старых значений количества
old_quantity = {}

# Приход
#Создание прихода
@receiver(pre_save, sender=ArrivalProduct)
def capture_old_quantity(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_quantity[instance.pk] = old_instance.quantity
        except sender.DoesNotExist:
            old_quantity[instance.pk] = 0

# Изменение прихода
@receiver(post_save, sender=ArrivalProduct)
def update_stock_on_arrival_product_save(sender, instance, created, **kwargs):
    original_quantity = old_quantity.pop(instance.pk, 0)
    if created:
        instance.product.quantity_in_stock += instance.quantity
    else:
        quantity_change = instance.quantity - original_quantity
        instance.product.quantity_in_stock += quantity_change
    instance.product.save()

# Удаление прихода
@receiver(post_delete, sender=ArrivalProduct)
def update_stock_on_arrival_product_delete(sender, instance, **kwargs):
    instance.product.quantity_in_stock -= instance.quantity
    instance.product.save()

# Перемещение
#Создание перемещения
@receiver(pre_save, sender=TransferProduct)
def capture_old_quantity_transfer(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_quantity[instance.pk] = old_instance.quantity
        except sender.DoesNotExist:
            old_quantity[instance.pk] = 0
# изменение перемещения
@receiver(post_save, sender=TransferProduct)
def update_stock_on_transfer_product_save(sender, instance, created, **kwargs):
    original_quantity = old_quantity.pop(instance.pk, 0)
    if created:
        # Для новых объектов просто уменьшаем количество на складе
        instance.product.quantity_in_stock -= instance.quantity
    else:
        # Для существующих объектов рассчитываем разницу и корректируем количество на складе
        quantity_change = instance.quantity - original_quantity
        instance.product.quantity_in_stock -= quantity_change
    instance.product.save()

# удаление перемещения
@receiver(post_delete, sender=TransferProduct)
def update_stock_on_transfer_product_delete(sender, instance, **kwargs):
    instance.product.quantity_in_stock += instance.quantity
    instance.product.save()

# Продажа
#Созадние продажи
@receiver(pre_save, sender=SaleProduct)
def capture_old_quantity_sale(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_quantity[instance.pk] = old_instance.quantity
        except sender.DoesNotExist:
            old_quantity[instance.pk] = 0

#Изменение продажи
@receiver(post_save, sender=SaleProduct)
def update_stock_on_sale_product_save(sender, instance, created, **kwargs):
    original_quantity = old_quantity.pop(instance.pk, 0)
    if created:
        # Для новых объектов просто уменьшаем количество на складе
        instance.product.quantity_in_stock -= instance.quantity
    else:
        # Для существующих объектов рассчитываем разницу и корректируем количество на складе
        quantity_change = original_quantity - instance.quantity
        instance.product.quantity_in_stock += quantity_change
    instance.product.save()

#Удаление продажи
@receiver(post_delete, sender=SaleProduct)
def update_stock_on_sale_product_delete(sender, instance, **kwargs):
    instance.product.quantity_in_stock += instance.quantity
    instance.product.save()
