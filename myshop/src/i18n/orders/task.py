from celery import task
from django.core.mail import send_mail

from orders.models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                                               order_id)
    mail_sent = send_mail(subject, message, '123@123.com', [order.email])
    print(mail_sent, type(mail_sent))
    return mail_sent