import threading

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend


class MultiSMTPBackend(EmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """

    def get_email_server(self, backend):
        return getattr(settings, 'EMAIL_BACKENDS', {}).get(backend, {})

    # pylint: disable=too-many-arguments, unused-argument
    def __init__(self, host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False,
                 use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None, use_backend='default', **kwargs):

        _server = self.get_email_server(use_backend)
        self.fail_silently = fail_silently

        self.host = _server.get('HOST', host)
        self.port = _server.get('PORT', port)
        self.username = _server.get('HOST_USER', username)
        self.password = _server.get('HOST_PASS', password)
        self.use_tls = _server.get('USE_TLS', use_tls)
        self.use_ssl = _server.get('USE_SSL', use_ssl)
        self.timeout = _server.get('TIMEOUT', timeout)
        self.ssl_keyfile = _server.get('SSL_KEYFILE', ssl_keyfile)
        self.ssl_certfile = _server.get('SSL_CERTFILE', ssl_certfile)
        if self.use_ssl and self.use_tls:
            raise ValueError(
                "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set "
                "one of those settings to True."
            )
        self.connection = None
        self._lock = threading.RLock()
