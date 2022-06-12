from smtplib import SMTPException

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.module_loading import import_string

import graphene

from graphql_jwt.decorators import token_auth

from graphql_auth.forms import RegisterForm,  PasswordLessRegisterForm
from graphql_auth.bases import Output
from graphql_auth.models import UserStatus
from graphql_auth.settings import graphql_auth_settings as app_settings
from graphql_auth.exceptions import  EmailAlreadyInUse
from core.constants import ErrorMessages
from graphql_auth.utils import using_refresh_tokens
from graphql_auth.signals import user_registered


UserModel = get_user_model()
if app_settings.EMAIL_ASYNC_TASK and isinstance(app_settings.EMAIL_ASYNC_TASK, str):
    async_email_func = import_string(app_settings.EMAIL_ASYNC_TASK)
else:
    async_email_func = None

# override the graphql_auth RegisterMixin to add the custom fields
class RegisterMixin(Output):
    """
    override the graphql_auth RegisterMixin to add the custom fields
    
    Register user with fields defined in the settings.

    If the email field of the user model is part of the
    registration fields (default), check if there is
    no user with that email or as a secondary email.

    If it exists, it does not register the user,
    even if the email field is not defined as unique
    (default of the default django user model).

    When creating the user, it also creates a `UserStatus`
    related to that user, making it possible to track
    if the user is archived, verified and has a secondary
    email.

    Send account verification email.

    If allowed to not verified users login, return token.
    """

    form = (
        PasswordLessRegisterForm
        if app_settings.ALLOW_PASSWORDLESS_REGISTRATION
        else RegisterForm
    )

    @classmethod
    def Field(cls, *args, **kwargs):
        if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
            if using_refresh_tokens():
                cls._meta.fields["refresh_token"] = graphene.Field(graphene.String)
            cls._meta.fields["token"] = graphene.Field(graphene.String)
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def login_on_register(cls, root, info, **kwargs):
        return cls()

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                f = cls.form(kwargs)
                # print(f)
                if f.is_valid():
                    email = kwargs.get(UserModel.EMAIL_FIELD, False)
                    medical_specialty = kwargs["medical_specialty"]
                    UserStatus.clean_email(email)
                    user = f.save()
                    user.medical_specialty.set(medical_specialty)
                    send_activation = (
                        app_settings.SEND_ACTIVATION_EMAIL is True and email
                    )
                    send_password_set = (
                        app_settings.ALLOW_PASSWORDLESS_REGISTRATION is True
                        and app_settings.SEND_PASSWORD_SET_EMAIL is True
                        and email
                    )
                    print(send_activation)
                    print("send_password_set", send_password_set)
                    if send_activation:
                        # TODO CHECK FOR EMAIL ASYNC SETTING
                        if async_email_func:
                            async_email_func(user.status.send_activation_email, (info,))
                        else:
                            user.status.send_activation_email(info)

                    if send_password_set:
                        # TODO CHECK FOR EMAIL ASYNC SETTING
                        if async_email_func:
                            async_email_func(
                                user.status.send_password_set_email, (info,)
                            )
                        else:
                            user.status.send_password_set_email(info)

                    user_registered.send(sender=cls, user=user)

                    if app_settings.ALLOW_LOGIN_NOT_VERIFIED:
                        payload = cls.login_on_register(
                            root, info, password=kwargs.get("password1"), **kwargs
                        )
                        return_value = {}
                        for field in cls._meta.fields:
                            return_value[field] = getattr(payload, field)
                        print(return_value)
                        return cls(**return_value)
                    return cls(success=True)
                else:
                    return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(
                success=False,
                # if the email was set as a secondary email,
                # the RegisterForm will not catch it,
                # so we need to run UserStatus.clean_email(email)
                errors={UserModel.EMAIL_FIELD: ErrorMessages.EMAIL_IN_USE},
            )
        except SMTPException:
            return cls(success=False, errors=ErrorMessages.EMAIL_FAIL)

