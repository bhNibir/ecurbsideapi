import disease.schema
import graphene
import users.schema
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery


class Query(UserQuery, users.schema.Query, MeQuery, disease.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, disease.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
