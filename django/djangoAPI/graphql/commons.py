import graphene

# classes for inputs


class EQ(graphene.InputObjectType):
    _eq = graphene.Int(required=True)


class IDEQ(graphene.InputObjectType):
    id = EQ(required=True)


class TableType(graphene.ObjectType):
    name = graphene.String()
    ofType = graphene.String()
# "ofType": {
# "kind": "OBJECT",
# "name": "ProjectDetailsType",
# "ofType": null
# }
#  OR
# "ofType": {
# "kind": "LIST",
# "name": null,
# "ofType": {
#     "ofType": {
#     "name": "reconciliation_view"
#     }
# }
# }
