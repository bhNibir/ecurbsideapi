import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from treatment.schema import TreatmentType

from .models import Disease, DiseaseCategories


class DiseaseType(DjangoObjectType):
    class Meta:
        model = Disease
        fields = ("id", "disease_name", "disease_categories", "descriptions", "create_by", "created_at", "updated_at")
    
    treatments = graphene.List(TreatmentType)

    def resolve_treatments(self, info):
        return self.treatment_disease.all()

class DiseaseCategoriesType(DjangoObjectType):
    class Meta:
        model = DiseaseCategories
        fields = ("id", "name",)

class Query(graphene.ObjectType):
    diseases = graphene.List(DiseaseType)
    diseases_categories = graphene.List(DiseaseCategoriesType)
    disease_by_id = graphene.Field(DiseaseType, id=graphene.String(required=True))
    # disease_category_by_name = graphene.Field(DiseaseCategoriesType, name=graphene.String(required=True))


    def resolve_diseases(self, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            # Querying a list Diseases
            return Disease.objects.all()
        raise GraphQLError("Login Required!")
        
       
    
    def resolve_diseases_categories(self, info, **kwargs):
        # Querying a list of Disease Categories
        return DiseaseCategories.objects.all()

    def resolve_disease_by_id(self, info, id):
        # Querying a single Disease
        return Disease.objects.get(pk=id)
        

    # def resolve_disease_category_by_name(self, info, name):
    #     try:
    #         return DiseaseCategories.objects.get(name=name)
    #     except DiseaseCategories.DoesNotExist:
    #         return None


class CreateDisease(graphene.Mutation):
    disease = graphene.Field(DiseaseType)


    class Arguments:
        disease_name = graphene.String(required=True)
        disease_categories_id = graphene.List(graphene.ID , required=True)
        descriptions = graphene.String(required=True)
        

    @login_required
    def mutate(self, info, disease_name, descriptions, disease_categories_id):
        print(disease_categories_id)
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login Required To add a disease")

        disease = Disease(create_by=user, disease_name=disease_name, descriptions=descriptions)
        disease.save()
        disease.disease_categories.set(disease_categories_id)
        
        return CreateDisease(disease=disease)

        

# class UpdateTrack(graphene.Mutation):
#     track = graphene.Field(TrackType)

#     class Arguments:
#         track_id = graphene.Int(required= True)
#         title = graphene.String()
#         description = graphene.String()
#         url = graphene.String()
    
#     def mutate(self, info, title, description, url, track_id):
#         user = info.context.user
#         track = Track.objects.get(id= track_id)
#         if track.create_by != user:
#             raise GraphQLError("User not premitted To Update the Track")

#         track.title = title
#         track.description = description
#         track.url = url
#         track.save()
#         return UpdateTrack(track= track)



# class DeleteTrack(graphene.Mutation):
#     track_id = graphene.Int()

#     class Arguments:
#         track_id = graphene.Int(required=True)

#     def mutate(self, info, track_id):
#         user = info.context.user
#         track = Track.objects.get(id=track_id)

#         if track.create_by != user:
#              raise GraphQLError("User not premitted To Delete the Track")
#         track.delete()
#         return DeleteTrack(track_id=track_id)

# class CreateDisease(graphene.Mutation):
#     disease = graphene.Field(DiseaseType)

#     class Arguments:
#         disease_name = graphene.String(required=True)

#     @login_required
#     def mutate(self, info, disease_name):
#         user = info.context.user
#         if user.is_anonymous:
#             raise Exception("Not Loged in ! Login Now")
#         disease = Disease(user=user, disease_name=disease_name)
#         disease.save()
#         return CreateDisease(disease=disease)



class Mutation(graphene.ObjectType):
    create_disease= CreateDisease.Field()