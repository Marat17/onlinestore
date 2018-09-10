from celery import task
from django.core.mail import send_mail
from orders.models import Order


@app.task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order #{}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order number is {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject,
                          message,
                          "celerytest123@gmail.com",
                          [order.email])
    return mail_sent