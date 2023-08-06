# -*- coding: utf-8 -*-
from django_multi_mail_backend.backend.multi import MultiServerBackend
from django_multi_mail_backend.backend.ses import MultiSESBackend
from django_multi_mail_backend.backend.smtp import MultiSMTPBackend

__all__ = [
    'MultiServerBackend',
    'MultiSESBackend',
    'MultiSMTPBackend',
]
