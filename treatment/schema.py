import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Treatment, TreatmentCategories


class TreatmentType(DjangoObjectType):
    class Meta:
        model = Treatment
        fields = ("id", "disease","treatment_name", "other_name", "treatment_categories", "image", "descriptions", "create_by", "created_at", "updated_at")
        image_url = graphene.String()

    def resolve_image_url(self, info):        
        return info.context.build_absolute_uri(self.image.url)

class TreatmentCategoriesType(DjangoObjectType):
    class Meta:
        model = TreatmentCategories
        fields = ("id", "name",)

class Query(graphene.ObjectType):
    treatments = graphene.List(TreatmentType)
    treatments_categories = graphene.List(TreatmentCategoriesType)
    treatment_by_id = graphene.Field(TreatmentType, id=graphene.String(required=True))
    treatment_by_disease_id = graphene.List(TreatmentType, disease_id=graphene.String(required=True))
    treatment_category_by_name = graphene.Field(TreatmentCategoriesType, name=graphene.String(required=True))


    def resolve_treatments(self, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Treatments
            return Treatment.objects.all()
        raise GraphQLError("Login Required!")
        
       
    
    def resolve_treatments_categories(self, info, **kwargs):
        # Querying a list of Treatment Categories
        return TreatmentCategories.objects.all()

    def resolve_treatment_by_id(self, info, id):
        # Querying a single Disease
        return Treatment.objects.get(pk=id)
    
    def resolve_treatment_by_disease_id(self, info, disease_id):
        # Querying a single Disease
        print("disease_id", disease_id)
        return Treatment.objects.filter(disease__id=disease_id)
        

    def resolve_treatment_category_by_name(self, info, name):
        try:
            return TreatmentCategories.objects.get(name=name)
        except TreatmentCategories.DoesNotExist:
            return None


# class CreateDisease(graphene.Mutation):
#     disease = graphene.Field(TreatmentType)


#     class Arguments:
#         disease_name = graphene.String(required=True)
#         disease_categories_id = graphene.List(graphene.ID , required=True)
#         descriptions = graphene.String(required=True)
        

#     @login_required
#     def mutate(self, info, disease_name, descriptions, disease_categories_id):
#         print(disease_categories_id)
#         user = info.context.user
#         if user.is_anonymous:
#             raise GraphQLError("Login Required To add a disease")

#         disease = Disease(create_by=user, disease_name=disease_name, descriptions=descriptions)
#         disease.save()
#         disease.disease_categories.set(disease_categories_id)
        
#         return CreateDisease(disease=disease)





# class Mutation(graphene.ObjectType):
#     create_disease= CreateDisease.Field()