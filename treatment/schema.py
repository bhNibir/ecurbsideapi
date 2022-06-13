from django.db import IntegrityError
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Treatment, TreatmentCategories
from django.db.models import Avg
from review.models import Review


class TreatmentReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("id", "rating", "content", "treatment", "create_by", "created_at", "updated_at")
        convert_choices_to_enum = False

class TreatmentType(DjangoObjectType):
    class Meta:
        model = Treatment
        fields = ("id", "disease","treatment_name", "other_name", "treatment_categories", "descriptions", "create_by", "created_at", "updated_at")
    
    
    image_url = graphene.String()
    total_reviews = graphene.Int()
    avg_rating = graphene.Int()
    reviews = graphene.List(TreatmentReviewType)


    def resolve_reviews(self, info):
        return self.fk_review_treatment.all()


    def resolve_image_url(self, info):    

        if self.image:
            return info.context.build_absolute_uri(self.image.url)


    def resolve_total_reviews(self, info):
        return self.fk_review_treatment.count()


    def resolve_avg_rating(self, info):
        rating_obj = self.fk_review_treatment.aggregate(Avg('rating'))

        return rating_obj["rating__avg"]

        

class TreatmentCategoriesType(DjangoObjectType):
    class Meta:
        model = TreatmentCategories
        fields = ("id", "name",)

class Query(graphene.ObjectType):
    treatments = graphene.List(TreatmentType)
    treatments_categories = graphene.List(TreatmentCategoriesType)
    treatment_by_id = graphene.Field(TreatmentType, id=graphene.String(required=True))
    # treatment_by_disease_id = graphene.List(TreatmentType, disease_id=graphene.String(required=True))
    # treatment_category_by_name = graphene.Field(TreatmentCategoriesType, name=graphene.String(required=True))


    def resolve_treatments(self, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Treatments
            return Treatment.objects.all().order_by("-id")
        raise GraphQLError("Login Required!")
        
       
    
    def resolve_treatments_categories(self, info, **kwargs):
        # Querying a list of Treatment Categories
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Treatments
            return TreatmentCategories.objects.all()
        raise GraphQLError("Login Required!")
        
       

    def resolve_treatment_by_id(self, info, id):
        # Querying a single Treatment
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Treatments
            return Treatment.objects.get(pk=id)
        raise GraphQLError("Login Required!")
        
        
    
    # def resolve_treatment_by_disease_id(self, info, disease_id):
    #     # Querying a single Disease
    #     print("disease_id", disease_id)
    #     return Treatment.objects.filter(disease__id=disease_id)
        

    # def resolve_treatment_category_by_name(self, info, name):
    #     try:
    #         return TreatmentCategories.objects.get(name=name)
    #     except TreatmentCategories.DoesNotExist:
    #         return None


class CreateTreatment(graphene.Mutation):
    treatment = graphene.Field(TreatmentType)


    class Arguments:
        treatment_name = graphene.String(required=True)
        other_name = graphene.String()
        treatment_category_id = graphene.ID(required=True)
        disease_id = graphene.ID(required=True)
        descriptions = graphene.String(required=True)
        

    @login_required
    def mutate(self, info, treatment_name, descriptions, treatment_category_id, other_name, disease_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login Required!")
        
        else:
            try:
                treatment = Treatment(create_by=user, treatment_name=treatment_name, descriptions=descriptions, other_name=other_name, disease_id=disease_id, treatment_categories_id = treatment_category_id)
                treatment.save()
                return CreateTreatment(treatment=treatment)

            except IntegrityError as e:
                if 'unique constraint' in str(e.args).lower():
                    raise GraphQLError(f'{treatment_name} is already there! Please Try Different.')  






class Mutation(graphene.ObjectType):
    create_treatment= CreateTreatment.Field()