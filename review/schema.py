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
        rating = graphene.Int(required=True)
        content = graphene.String(required=True)
        treatment_id = graphene.ID(required=True)
       

    @login_required
    def mutate(self, info, rating, content, treatment_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login Required To add a treatment")
        
        review = Review(create_by=user, treatment_id=treatment_id, rating=rating, content=content)
        review.save()
        
        return CreateReview(review=review)





class Mutation(graphene.ObjectType):
    create_review = CreateReview.Field()