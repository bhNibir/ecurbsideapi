import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Review, ReviewComment, ReviewLike




class ReviewType(DjangoObjectType):
   
    class Meta:
        model = Review
        fields = ("id", "rating", "content", "treatment", "create_by", "created_at", "updated_at")
        
        

   

class Query(graphene.ObjectType):
      
    reviews_by_id = graphene.Field(ReviewType, id=graphene.String(required=True))


    def resolve_treatment_by_id(self, info, id):
        user = info.context.user
        if user.is_authenticated:
             # Querying a single Treatment
            return Review.objects.get(pk=id)
        raise GraphQLError("Login Required!")
       
        
        

   

class CreateReview(graphene.Mutation):
    review = graphene.Field(ReviewType)


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
            raise GraphQLError("Login Required To add a treatment")
        
        treatment = Review(create_by=user, treatment_name=treatment_name, descriptions=descriptions, other_name=other_name, disease_id=disease_id, treatment_categories_id = treatment_category_id)
        treatment.save()
        
        return CreateReview(treatment=treatment)





class Mutation(graphene.ObjectType):
    create_review = CreateReview.Field()