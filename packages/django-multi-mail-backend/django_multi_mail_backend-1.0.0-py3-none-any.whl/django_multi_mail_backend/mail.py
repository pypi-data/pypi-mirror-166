from django.core.mail import get_connection

from django_multi_mail_backend.message import EmailMessage, EmailMultiAlternatives


def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, backend='default'):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
        backend=backend or 'default'
    )
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()


def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None,
                   backend='default'):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), send
    each message to each recipient list. Return the number of emails sent.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user and auth_password are set, use them to log in.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
        backend=backend or 'default'
    )
    messages = [
        EmailMessage(subject, message, sender, recipient, connection=connection)
        for subject, message, sender, recipient in datatuple
    ]
    return connection.send_messages(messages)
