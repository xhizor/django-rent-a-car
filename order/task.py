from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from celery import task
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Order


@task
def order_created(pk):
    order = Order.objects.get(pk=pk)
    subject = 'Rent-a-car Order detail'
    message = f'Your Order #{order.pk} is successfully paid. Enjoy driving & Good luck!'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
    email.send()
    return True


@task
def send_pdf_to_email(pk):
    order = Order.objects.get(pk=pk)
    html = render_to_string('order/order_detail_pdf.html', {'order': order})
    out = BytesIO()
    HTML(string=html).write_pdf(out)

    subject = 'Rent-a-car Order detail'
    message = f'We approved your Order #{order.pk}. You can see Order detail in PDF attachment. ' \
              'Thank you for using our Rent-a-car service!'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.user.email])
    email.attach('Order #{}_{}.pdf'.format(order.pk, order.car.name),
                 out.getvalue(), 'application/pdf')
    email.send()
    return True