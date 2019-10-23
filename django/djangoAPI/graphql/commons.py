import graphene

# classes for inputs


class EQ(graphene.InputObjectType):
    _eq = graphene.Int(required=True)


class IDEQ(graphene.InputObjectType):
    id = EQ(required=True)
