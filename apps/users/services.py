from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from apps.common.uid import encode_uid


mail_confirm_content = _(
    """Hi there,

Thanks for signing up to "Be My Guest"!

Before you can start using the system, you'll need to confirm your email. To confirm, click the link below and log into your account with the details you signed up with.

{url}

See you soon!
"""
)


def send_mail_with_confirm_token(user):
    """
    Generate a token for a user to validate its email address
    and thus its account.
    Prior to the confirmation of its account, User is set as non active.
    (User.is_active = False)
    """
    confirm_token = default_token_generator.make_token(user)
    url = "/".join((settings.FRONT_BASE_URL, "auth", confirm_token, ""))
    send_mail(
        _("Confirm your email"),
        mail_confirm_content.format(url=url),
        "do-not-reply@bemyguest.com",
        [user.email],
        fail_silently=False,
    )


mail_forgotten_password_content = _(
    """Hello,

We have recently received a request to change the password of your BeMyGuest account.

If you are the originator of this request, you can set a new password here:

{url}

If you do not want to change your password or if you are not the source of this request, you can ignore this message and delete it.

To avoid compromising the security of your account, please do not forward this email to anyone.

Cheers!
"""
)


def send_reset_password_mail(user):
    """
    Generate a token for a user to reset its password
    and send an email with it
    """
    token = default_token_generator.make_token(user)
    url = "/".join(
        (
            settings.FRONT_BASE_URL,
            "password-reset-confirm",
            encode_uid(user.id),
            token,
            "",
        )
    )
    send_mail(
        _("Reset your password"),
        mail_confirm_content.format(url=url),
        "do-not-reply@bemyguest.com",
        [user.email],
        fail_silently=False,
    )


def set_password_user(user, password):
    user.set_password(password)
    user.save()


def activate_user(user):
    user.is_active = True
    user.save()
    return user
