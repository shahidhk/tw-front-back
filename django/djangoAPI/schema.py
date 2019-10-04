'''Defines the GraphQL Queries and Mutations'''

import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType

from djangoAPI.models import *
from djangoAPI.apiUtils import *


class ReconViewType(DjangoObjectType):
    class Meta:
        model = ReconciliationView


class InsertReconViewInput(graphene.InputObjectType):
    role_number = graphene.String(required=True)
    role_name = graphene.String(required=True)
    parent = graphene.Int(required=True)
    # TODO change below to required=True eventually
    role_criticality = graphene.Int(required=False)
    role_priority = graphene.Int(required=False)
    role_spatial_site_id = graphene.Int(required=False)


class InsertReconciliationView(graphene.Mutation):
    class Arguments:
        objects = InsertReconViewInput(required=True)

    returning = graphene.Field(ReconViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        if objects is None:
            return 'No object specified'
        role_data = {
            'role_number': objects.role_number,
            'role_spatial_site_id': 1,  # objects.role_spatial_site_id
            'role_priority': 1,  # objects.role_priority
            'role_name': objects.role_name,
            'role_criticality': 1,  # objects.role_criticality
            'parent_id': objects.parent,
        }
        new_entity = MissingRoleUtil(role_data)
        if new_entity['result'] == 0:
            new_entity = ReconciliationView.objects.get(
                pk=new_entity['errors'])
            return InsertReconciliationView(returning=new_entity)
        raise GraphQLError(new_entity['errors'])


class UnassAssViewType(DjangoObjectType):
    class Meta:
        model = UnassignedAssetsView


class Query(ObjectType):
    reconciliation_view = graphene.List(ReconViewType)
    unassigned_assets = graphene.List(UnassAssViewType)

    def resolve_reconciliation_view(self, info, **kwargs):
        return ReconciliationView.objects.all()

    def resolve_all_avantis(self, info, **kwargs):
        return UnassignedAssetsView.objects.all()


class Mutations(graphene.ObjectType):
    insert_reconciliation_view = InsertReconciliationView.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
