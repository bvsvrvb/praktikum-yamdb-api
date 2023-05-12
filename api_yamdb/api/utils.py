from django.core.mail import send_mail

from api_yamdb import settings


def to_send_mail(code, email):
    send_mail(
        'Код авторизации на Yamdb',
        f'Ваш код для авторизации: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
