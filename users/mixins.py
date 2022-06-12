from smtplib import SMTPException

from django.core.signing import BadSignature, SignatureExpired
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.db import transaction
from django.utils.module_loading import import_string

import graphene

from graphql_jwt.exceptions import JSONWebTokenError, JSONWebTokenExpired
from graphql_jwt.decorators import token_auth

from graphql_auth.forms import RegisterForm, EmailForm, UpdateAccountForm, PasswordLessRegisterForm
from graphql_auth.bases import Output
from graphql_auth.models import UserStatus
from graphql_auth.settings import graphql_auth_settings as app_settings
from graphql_auth.exceptions import (
    UserAlreadyVerified,
    UserNotVerified,
    WrongUsage,
    TokenScopeError,
    EmailAlreadyInUse,
    InvalidCredentials,
    PasswordAlreadySetError,
)
from graphql_auth.constants import Messages, TokenAction
from graphql_auth.utils import revoke_user_refresh_token, get_token_paylod, using_refresh_tokens
from graphql_auth.shortcuts import get_user_by_email, get_user_to_login
from graphql_auth.signals import user_registered, user_verified
from graphql_auth.decorators import (
    password_confirmation_required,
    verification_required,
    secondary_email_required,
)

UserModel = get_user_model()
if app_settings.EMAIL_ASYNC_TASK and isinstance(app_settings.EMAIL_ASYNC_TASK, str):
    async_email_func = import_string(app_settings.EMAIL_ASYNC_TASK)
else:
    async_email_func = None

class RegisterMixin(Output):
    """
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
                username = kwargs["username"]
                email = kwargs.get(UserModel.EMAIL_FIELD, False)
                password = kwargs["username"]
                first_name = kwargs["first_name"]
                last_name = kwargs["last_name"]
                country = kwargs["country"]
                health_provider = kwargs["health_provider"]
                medical_provider_type = kwargs["medical_provider_type"] 
                medical_specialty = kwargs["medical_specialty"]
                medical_setting = kwargs["medical_setting"] 

                UserStatus.clean_email(email)
                user = UserModel(
                    username=username, 
                    email=email, 
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    health_provider=health_provider,
                    medical_setting_id=medical_setting,
                    medical_provider_type_id=medical_provider_type,
                    )
                user.set_password(password)
                user.save()
                user.medical_specialty.set(medical_specialty)
                
                send_activation = (
                    app_settings.SEND_ACTIVATION_EMAIL is True and email
                )
              
                print(send_activation)
                if send_activation:
                    # TODO CHECK FOR EMAIL ASYNC SETTING
                    if async_email_func:
                        async_email_func(user.status.send_activation_email, (info,))
                    else:
                        user.status.send_activation_email(info)

                user_registered.send(sender=cls, user=user)
                return cls(success=True)
                # if f.is_valid():
                   
                # else:
                #     return cls(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return cls(
                success=False,
                # if the email was set as a secondary email,
                # the RegisterForm will not catch it,
                # so we need to run UserStatus.clean_email(email)
                errors={UserModel.EMAIL_FIELD: Messages.EMAIL_IN_USE},
            )
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)

