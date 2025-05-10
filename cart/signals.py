from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItems

@receiver(post_save, sender=CartItems)
def update_cart_total_on_save(sender, instance, **kwargs):
    instance.cart.update_total()

@receiver(post_delete, sender=CartItems)
def update_cart_total_on_delete(sender, instance, **kwargs):
    instance.cart.update_total()
