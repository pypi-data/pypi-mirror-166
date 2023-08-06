# -*- coding: utf-8 -*-
from django_multi_mail_backend.mail import get_connection, send_mail, send_mass_mail
from django_multi_mail_backend.message import EmailMessage, EmailMultiAlternatives

__all__ = [
    'send_mail',
    'send_mass_mail',
    'get_connection',
    'EmailMessage',
    'EmailMultiAlternatives',
]
