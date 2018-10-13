from django.contrib.auth.tokens import default_token_generator

from apps.common.uid import encode_uid


def send_mail_with_confirm_token(user):
    """
    Generate a token for a user to validate its email address
    and thus its account.
    Prior to the confirmation of its account, User is set as non active.
    (User.is_active = False)
    """
    confirm_token = default_token_generator.make_token(user)
    # emails.confirm(user, confirm_token)


def send_reset_password_mail(user):
    """
    Generate a token for a user to reset its password
    and send an email with it
    """
    token = default_token_generator.make_token(user)
    # emails.reset_password(user, token, encode_uid(user.id))


def set_password_user(user, password):
    user.set_password(password)
    user.save()


def activate_user(user):
    user.is_active = True
    user.save()
