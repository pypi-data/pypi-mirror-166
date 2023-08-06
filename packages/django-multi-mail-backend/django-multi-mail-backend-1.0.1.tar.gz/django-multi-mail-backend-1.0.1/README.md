Django Multi Mail Backend
=

If you use or like the project, click `Star` and `Watch` to generate metrics and i evaluate project continuity.

# Install:
    pip install django-multi-mail-backend

# Configuration
1. Usage with multi backend
    1. In your `settings.py`:
        ```
        EMAIL_BACKEND = 'django_multi_mail_backend.backend.MultiServerBackend'
        ```
    
    1. set settings servers backend, in `settings.py`, ex:
        ```
        EMAIL_BACKENDS = {
            'smtp': {
                'BACKEND': 'django_multi_mail_backend.backend.MultiSMTPBackend',
                # settings for MultiSMTPBackend
            },
            'smtp2': {
                'BACKEND': 'django_multi_mail_backend.backend.MultiSMTPBackend',
                # settings for MultiSMTPBackend
            },
            'ses': {
                'BACKEND': 'django_multi_mail_backend.backend.MultiSESBackend',
                # settings for MultiSESBackend
            },
            'original_smtp': {
                'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                # this use original django smtp class and configurations
            },
            'console': {
                'BACKEND': 'django.core.mail.backends.console.EmailBackend',
            }
        }
        ```

1. Multi SMTP Server:

    1. In your `settings.py`:
        ```
        EMAIL_BACKEND = 'django_multi_mail_backend.backend.MultiSMTPBackend'
        ```
    
    1. set settings for MultiSMTPBackend in `settings.py`:
        ```
        # MultiSMTPBackend use django `django.core.mail.backends.smtp.EmailBackend` in the background
        EMAIL_BACKENDS = {
            'default': {
                # see all configuration here: https://docs.djangoproject.com/en/4.1/topics/email/#smtp-backend
                'HOST': 'mailhog',
                'PORT': 1025,
                'HOST_USER': None,
                'HOST_PASS': None,
                'USE_TLS': None,
                'USE_SSL': None,
                'TIMEOUT': None,
                'SSL_KEYFILE': None,
                'SSL_CERTFILE': None,
                'DEFAULT_FROM_EMAIL': "test@teste.com",
            },
            'example1': {
                # copy above settings
            }
        }
        ```

1. Multi SES Server:

    1. In your `settings.py`:
        ```
        EMAIL_BACKEND = 'django_multi_mail_backend.backend.MultiSESBackend'
        ```
    
    1. set settings for MultiSESBackend in `settings.py`:
        ```
        # MultiSESBackend use django `django_ses.SESBackend` in the background
        # see all configuration here: https://github.com/django-ses/django-ses
        # removed `AWS_` in front of the keys
        EMAIL_BACKENDS = {
            'default': {
                'ACCESS_KEY': 'mailhog',
                'SECRET_KEY': 1025,
                'SESSION_TOKEN': None,
                'SES_REGION_NAME': None,
                'SES_REGION_ENDPOINT_URL': None,
                'SES_AUTO_THROTTLE': None,
                'SES_CONFIG': None,
                'DKIM_DOMAIN': None,
                'DKIM_PRIVATE_KEY': None,
                'DKIM_SELECTOR': None,
                'DKIM_HEADERS': None,
                'SES_SOURCE_ARN': None,
                'SES_FROM_ARN': None,
                'SES_RETURN_PATH_ARN': None,
            },
            'example1': {
                # copy above settings
            }
        }
        ```

# Usage

Don't use default django methods direct, because this method not accept custom parameters,
instead use the options below

1. With send_mail
    ```
        from django_multi_mail_backend import send_mail, send_mass_mail
        ...

        send_mail(..., use_use_backend='smtp')
        send_mass_mail(..., use_backend='ses')
    ```
    or
    ```
        from django.core.mail import send_mail, send_mass_mail, get_connection
        ...

        with get_connection(use_backend='console') as connection:
            send_mail(..., connection=connection)
            send_mass_mail(..., connection=connection)
    ```

1. With EmailMessage
    ```
    from django_multi_mail_backend import EmailMessage, EmailMultiAlternatives
    ...

    EmailMessage(..., use_backend='smtp2').send()
    EmailMultiAlternatives(..., use_backend='original_smtp').send()
    ```
    or 
    ```
    from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
    ...

    with get_connection(use_backend='smtp') as connection:
        EmailMessage(..., connection=connection).send()
        EmailMultiAlternatives(..., connection=connection).send()
    ```

1. With send_messages
    ```
    from django_multi_mail_backend import EmailMessage, EmailMultiAlternatives, get_connection
    ...

    with get_connection(use_backend='smtp') as connection:
        connection.send_messages([EmailMessage(...), EmailMultiAlternatives(...)])
    ```
    or
    ```
    from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection
    ...

    with get_connection(use_backend='smtp') as connection:
        connection.send_messages([EmailMessage(...), EmailMultiAlternatives(...)])
    ```