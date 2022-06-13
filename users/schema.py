import graphene
from django_countries.graphql.types import Country
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_auth import mutations
from django_countries import countries
from disease.models import FavoriteDisease

from disease.schema import  FavoriteDiseaseType
from .models import (CustomUser, MedicalProvider, MedicalSetting)
from graphql_auth.bases import MutationMixin
from .mixins import RegisterMixin




class CustomUserType(DjangoObjectType):
   
    class Meta:
        model = CustomUser
        fields = ("id", "username", 'email', 'first_name', 'last_name' , 'profile_picture', 'country', 'health_provider', 'medical_provider_type', 'medical_specialty', 'medical_setting',)
    

    profile_picture = graphene.String()
    country = graphene.Field(Country)
    health_provider = graphene.Boolean()


    def resolve_profile_picture(self, info):    

        if self.profile_picture:
            return info.context.build_absolute_uri(self.profile_picture.url)



class MedicalProviderType(DjangoObjectType):
    class Meta:
        model = MedicalProvider
        fields = ("id", "name")


class MedicalSettingType(DjangoObjectType):
    class Meta:
        model = MedicalSetting
        fields = ("id",  "name")


   
class Query(graphene.ObjectType):
    # user = graphene.Field(CustomUserType)
    # users = DjangoFilterConnectionField(CustomUserType)
    me = graphene.Field(CustomUserType)

    
    medical_setting = graphene.List(MedicalSettingType)
    medical_provider = graphene.List(MedicalProviderType)
    country_list = graphene.List(Country)
    favorite_disease_list = graphene.List(FavoriteDiseaseType)
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        raise GraphQLError("Login Required!")

    def resolve_medical_setting(self, info, **kwargs):
        # Querying a list of Medical Setting
        return MedicalSetting.objects.all()


    def resolve_medical_provider(self, info, **kwargs):
        # Querying a list of Medical Provider
        return MedicalProvider.objects.all()


    def resolve_country_list(self, info, **kwargs):
        # Querying a list of Countries
        return list(countries)


    def resolve_favorite_disease_list(self, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Treatments
            return FavoriteDisease.objects.filter(user_id=user.id)
        raise GraphQLError("Login Required!")


class UserRegistration(MutationMixin, RegisterMixin, graphene.Mutation): 

    #that will be used to register a new user based on graphql_auth
    class Arguments:
        username = graphene.String(required=True)
        email= graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        country = graphene.String(required=True)
        health_provider = graphene.Boolean(required=True)
        medical_provider_type = graphene.ID()
        medical_specialty = graphene.List(graphene.ID)
        medical_setting = graphene.ID()

class Mutation(graphene.ObjectType):
    # user_registration is custom mutation class
    user_registration = UserRegistration.Field()

    # graphql_auth provide mutations classes
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


