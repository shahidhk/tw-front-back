'''Defines the GraphQL Queries and Mutations'''

import graphene
from pprint import pprint
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.rest_framework.serializer_converter import convert_serializer_to_input_type

from rest_framework import serializers

from djangoAPI.models import *
from djangoAPI.apiUtils import *

# classes for outputs


class ReconViewType(DjangoObjectType):
    class Meta:
        model = ReconciliationView


class UnassAssViewType(DjangoObjectType):
    class Meta:
        model = UnassignedAssetsView


class UnassAssViewTypeDeleted(graphene.ObjectType):
    asset_serial_number = graphene.String()
    id = graphene.Int()


class ReservationViewType(DjangoObjectType):
    class Meta:
        model = ReservationView


# classes for inputs
class EQ(graphene.InputObjectType):
    _eq = graphene.Int(required=True)


class IDEQ(graphene.InputObjectType):
    id = EQ(required=True)

# Roundabout way to create fields for input in recon and asset view
# see https://github.com/graphql-python/graphene-django/issues/121


class ReconViewSerial(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationView
        # the id is excluded since the client will never be able to specify the primary key, it will be returned once the entry is generated on the db
        exclude = ('id',)


class ReconciliationViewSet(convert_serializer_to_input_type(ReconViewSerial)):
    role_id = graphene.Int()


class UnassViewSerial(serializers.ModelSerializer):
    class Meta:
        model = UnassignedAssetsView
        exclude = ('id',)


class UnassViewSet(convert_serializer_to_input_type(UnassViewSerial)):
    role_id = graphene.Int()


class ReserViewSerial(serializers.ModelSerializer):
    class Meta:
        model = ReservationView
        exclude = ('id',)


class ReserViewSet(convert_serializer_to_input_type(ReserViewSerial)):
    pass


# recon view mutations
class UpdateReconView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = ReconciliationViewSet(required=True)

    returning = graphene.Field(ReconViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        # call different functions depending on what is changed
        # TODO allow changing multiple columns at the same time
        if not _set.role_exists is None:
            data = {'role_id': where.id._eq,
                    'entity_exists': _set.role_exists,
                    }
            data = DoesNotExistUtil(data)
        elif not _set.parent is None:
            data = {'role_id': where.id._eq,
                    'parent_id': _set.parent,
                    }
            data = RoleParentUtil(data)
        elif not _set.asset_id is None:
            data = {'role_id': where.id._eq,
                    'asset_id': _set.asset_id,
                    }
            data = AssignAssetToRoleUtil(data)
        else:
            raise GraphQLError('Unimplimented')
        # Check the result of called function and return row on success
        if data['result'] == 0:
            data = ReconciliationView.objects.get(
                pk=data['errors'])
            return UpdateReconView(returning=data)
        raise GraphQLError(data['errors'])


class InsertReconciliationView(graphene.Mutation):
    class Arguments:
        objects = ReconciliationViewSet(required=True)

    returning = graphene.Field(ReconViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        role_data = {
            'role_number': objects.role_number,
            'role_spatial_site_id': 'a',  # objects.role_spatial_site_id
            'role_priority': 'a',  # objects.role_priority
            'role_name': objects.role_name,
            'role_criticality': 'a',  # objects.role_criticality
            'parent_id': objects.parent,
        }
        new_entity = MissingRoleUtil(role_data)
        if new_entity['result'] == 0:
            new_entity = ReconciliationView.objects.get(
                pk=new_entity['errors'])
            return InsertReconciliationView(returning=new_entity)
        raise GraphQLError(new_entity['errors'])


# unassigned asset mutations
class InsertUnassView(graphene.Mutation):
    class Arguments:
        objects = UnassViewSet(required=True)

    returning = graphene.Field(UnassAssViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        data = {'asset_serial_number': objects.asset_serial_number}
        data = MissingAssetUtil(data)
        if data['result'] == 0:
            data = UnassignedAssetsView.objects.get(
                pk=data['errors'])
            return InsertUnassView(returning=data)
        raise GraphQLError(data['errors'])


class UpdateUnassView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = UnassViewSet(required=True)
    # TODO not sure what should be returned since the entry disappears
    returning = graphene.Field(UnassAssViewTypeDeleted)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        data = {'role_id': _set.role_id,
                'asset_id': where.id._eq,
                }
        data = AssignAssetToRoleUtil(data)
        if data['result'] == 0:
            # data = UnassignedAssetsView.objects.get(
            #     pk=data['errors'])
            data = UnassAssViewTypeDeleted(id=where.id._eq)
            return InsertUnassView(returning=data)
        raise GraphQLError(data['errors'])


class DeleteUnassView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
    # TODO not sure what should be returned since the entry disappears
    returning = graphene.Field(UnassAssViewTypeDeleted)

    @staticmethod
    def mutate(root, info, where=None):
        data = {'asset_id': where.id._eq, }
        data = RetireAssetUtil(data)
        if data['result'] == 0:
            data = UnassAssViewTypeDeleted(
                id=where.id._eq, asset_serial_number=data['errors'])
            return InsertUnassView(returning=data)
        raise GraphQLError(data['errors'])


class UpdateReserView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = ReserViewSet(required=True)
    returning = graphene.List(ReservationViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        if not _set.reserved is None:
            data = {'id': where.id._eq, 'reserved': _set.reserved}
            data = ReserveEntityUtil(data, info)
        elif not _set.approved is None:
            data = {'id': where.id._eq, 'approved': _set.approved}
            data = ApproveReservationUtil(data, info)
        else:
            raise GraphQLError('Unimplimented')
        if data['result'] == 0:
            data = ReservationView.objects.filter(
                pk=data['errors'])
            return UpdateReserView(returning=data)
        raise GraphQLError(data['errors'])


class Query(ObjectType):
    reconciliation_view_2 = graphene.List(ReconViewType)
    unassigned_assets_2 = graphene.List(UnassAssViewType)

    def resolve_reconciliation_view_2(self, info, **kwargs):
        return ReconciliationView.objects.all()

    def resolve_all_avantis_2(self, info, **kwargs):
        return UnassignedAssetsView.objects.all()


class Mutations(graphene.ObjectType):
    insert_reconciliation_view = InsertReconciliationView.Field()
    update_reconciliation_view = UpdateReconView.Field()
    insert_unassigned_assets = InsertUnassView.Field()
    update_unassigned_assets = UpdateUnassView.Field()
    delete_unassigned_assets = DeleteUnassView.Field()
    update_reservation_view = UpdateReserView.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
