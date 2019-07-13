import graphene

from api_endpoint.schema import ApiQuery, ApiMutation


class Query(ApiQuery, graphene.ObjectType):
    pass


class Mutation(ApiMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
