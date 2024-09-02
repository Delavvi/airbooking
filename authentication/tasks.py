from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_activation_email(username, email, token, domain, pk):
    message = render_to_string('email_template.html', {
        'username': username,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(pk)),
        'token': token,
    })
    mail_subject = 'Activate your account.'
    send_mail(mail_subject, message, 'djangogramm96@gmail.com', [email], html_message=message)
