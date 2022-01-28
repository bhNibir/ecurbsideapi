import graphene
from django_countries.graphql.types import Country
from graphene_django import DjangoObjectType
from graphql_auth import mutations

from .models import (CustomUser, MedicalProvider, MedicalSetting,
                     ProfessionalProfile)


class CustomUserType(DjangoObjectType):
    country = graphene.Field(Country)
    class Meta:
        model = CustomUser
        fields = ("id", 'first_name', 'last_name' , 'country')

class MedicalProviderType(DjangoObjectType):
    class Meta:
        model = MedicalProvider
        # fields = ("id", )


class MedicalSettingType(DjangoObjectType):
    class Meta:
        model = MedicalSetting
        # fields = ("id", )
class ProfessionalProfileType(DjangoObjectType):
    class Meta:
        model = ProfessionalProfile
        fields = ('user', 'health_provider', 'medical_provider_type', 'medical_specialty', 'medical_setting', 'update_date')



class Query(graphene.ObjectType):
    user_profile_by_id = graphene.Field(ProfessionalProfileType, id=graphene.String())
 
    def resolve_user_profile_by_id(self, info, id):
        # Querying a single ProfessionalProfile
        return ProfessionalProfile.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    # send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    # verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    # swap_emails = mutations.SwapEmails.Field()
    # remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


