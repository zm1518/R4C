from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from orders.models import Order


@receiver(post_save)
def notify_customers(sender, instance, **kwargs):
    orders = Order.objects.filter(robot_serial=instance.serial)
    if orders.exists():
        for order in orders:
            context = {
                'model': instance.model,
                'version': instance.version
            }
            message = render_to_string('notification_email.txt', context)
            plain_text = strip_tags(message)
            send_mail('Робот доступен в наличии', plain_text, 'email@example.com', [order.customer.email])
