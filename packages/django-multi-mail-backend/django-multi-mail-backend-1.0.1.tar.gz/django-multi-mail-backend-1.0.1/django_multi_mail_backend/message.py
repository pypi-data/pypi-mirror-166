from django.core.mail import get_connection as get_mail_connection
from django.core.mail.message import EmailMessage as _EmailMessage
from django.core.mail.message import EmailMultiAlternatives as _EmailMultiAlternatives


class MultiServerMixin:

    def __init__(self, *args, use_backend='default', **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = use_backend or 'default'

    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = get_mail_connection(fail_silently=fail_silently, use_backend=self.backend)
        return self.connection


class EmailMessage(MultiServerMixin, _EmailMessage):
    pass


class EmailMultiAlternatives(MultiServerMixin, _EmailMultiAlternatives):
    pass
