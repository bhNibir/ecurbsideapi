from django_countries import countries
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required


from .models import Review, ReviewComment, ReviewLike
from django.db import IntegrityError
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from users.models import (MedicalProvider, DiseaseCategories)


class ReviewFilter(django_filters.FilterSet):
    country = django_filters.MultipleChoiceFilter(
        field_name='create_by__country', choices=list(countries))
    medical_provider = django_filters.ModelMultipleChoiceFilter(
        field_name='create_by__medical_provider_type__id', to_field_name='id', queryset=MedicalProvider.objects.all())
    medical_specialty = django_filters.ModelMultipleChoiceFilter(
        field_name='create_by__medical_specialty__id', to_field_name='id', queryset=DiseaseCategories.objects.all())
    treatment_id = django_filters.CharFilter(field_name='treatment__id')

    class Meta:
        model = Review
        fields = ("treatment", "create_by")

    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at',),
            ('rating', 'rating',),
        )
    )


class ReviewType(DjangoObjectType):

    class Meta:
        model = Review
        fields = ("id", "rating", "content", "treatment",
                  "create_by", "created_at", "updated_at")
        convert_choices_to_enum = False
        filterset_class = ReviewFilter
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):

    reviews_by_id = graphene.Field(
        ReviewType, id=graphene.String(required=True))
    reviews_by_treatment_id = DjangoFilterConnectionField(
        ReviewType,  id=graphene.String(required=True))

    def resolve_reviews_by_id(self, info, id):
        user = info.context.user
        if user.is_authenticated:
            # Querying a single Treatment
            return Review.objects.get(pk=id)
        raise GraphQLError("Login Required!")

 # Querying Reviews by TreatmentId
    def resolve_reviews_by_treatment_id(self, info, id, *args, **kwargs):
        user = info.context.user

        if user.is_authenticated:
            # return review List default filter by treatment_id

            kwargs['treatment_id'] = id
            # kwargs['country']=[x.upper() for x in kwargs['country']]
            # print("kwargs: ", kwargs)
            return ReviewFilter(kwargs).qs

        raise GraphQLError("Login Required!")


class CreateReview(graphene.Mutation):
    review = graphene.Field(ReviewType)

    class Arguments:
        rating = graphene.Int(required=True)
        content = graphene.String(required=True)
        treatment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, rating, content, treatment_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login Required!")

        else:
            try:

                review = Review(
                    create_by=user, treatment_id=treatment_id, rating=rating, content=content)
                review.save()
                return CreateReview(review=review)

            except IntegrityError as e:
                if 'unique constraint' in str(e.args).lower():
                    raise GraphQLError("You have already rated !")


class Mutation(graphene.ObjectType):
    create_review = CreateReview.Field()
