from importlib import import_module

from django.conf import settings


class MultiServerBackend:

    def get_email_server(self, server):
        return getattr(settings, 'EMAIL_BACKENDS', {}).get(server, {})

    def __init__(self, backend='default', **kwargs):
        _server = self.get_email_server(backend)
        backend = _server.get("BACKEND", "").split(".")

        mail_class = getattr(import_module('.'.join(backend[0:-1])), backend[-1])
        self.backend = mail_class(backend=backend, **kwargs)

    def __enter__(self):
        return self.backend.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.backend.__exit__(exc_type, exc_value, traceback)

    def __getattr__(self, name):
        return self.backend.__getattribute__(name)
