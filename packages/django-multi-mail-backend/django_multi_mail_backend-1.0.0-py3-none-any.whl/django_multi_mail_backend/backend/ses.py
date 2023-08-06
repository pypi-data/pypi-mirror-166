try:
    from django.conf import settings

    from django_ses import SESBackend, cast_nonzero_to_float
except Exception:
    settings = object
    SESBackend = object
    cast_nonzero_to_float = lambda x: x  # noqa


class MultiSESBackend(SESBackend):
    """
        A Django Email backend that uses Amazon's Simple Email Service.
    """

    def get_email_server(self, server):
        return getattr(settings, 'EMAIL_BACKENDS', {}).get(server, {})

    # pylint: disable=too-many-locals, too-many-arguments, unused-argument
    def __init__(self, fail_silently=False, aws_access_key=None, aws_secret_key=None, aws_session_token=None,
                 aws_region_name=None, aws_region_endpoint=None, aws_auto_throttle=None, aws_config=None,
                 dkim_domain=None, dkim_key=None, dkim_selector=None, dkim_headers=None, ses_source_arn=None,
                 ses_from_arn=None, ses_return_path_arn=None, backend='default', **kwargs):

        _server = self.get_email_server(backend)
        self.fail_silently = fail_silently

        self._access_key_id = _server.get('ACCESS_KEY', aws_access_key)
        self._access_key = _server.get('SECRET_KEY', aws_secret_key)
        self._session_token = _server.get('SESSION_TOKEN', aws_session_token)
        self._region_name = _server.get('SES_REGION_NAME', aws_region_name)
        self._endpoint_url = _server.get('SES_REGION_ENDPOINT_URL', aws_region_endpoint)
        self._throttle = cast_nonzero_to_float(_server.get('SES_AUTO_THROTTLE', aws_auto_throttle))
        self._config = _server.get('SES_CONFIG', aws_config)

        self.dkim_domain = _server.get('DKIM_DOMAIN', dkim_domain)
        self.dkim_key = _server.get('DKIM_PRIVATE_KEY', dkim_key)
        self.dkim_selector = _server.get('DKIM_SELECTOR', dkim_selector)
        self.dkim_headers = _server.get('DKIM_HEADERS', dkim_headers)

        self.ses_source_arn = _server.get('SES_SOURCE_ARN', ses_source_arn)
        self.ses_from_arn = _server.get('SES_FROM_ARN', ses_from_arn)
        self.ses_return_path_arn = _server.get('SES_RETURN_PATH_ARN', ses_return_path_arn)

        self.connection = None
