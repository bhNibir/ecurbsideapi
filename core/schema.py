import disease.schema
import graphene
import users.schema
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery
import treatment.schema


class Query(UserQuery, users.schema.Query, MeQuery, disease.schema.Query, treatment.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, disease.schema.Mutation, treatment.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
