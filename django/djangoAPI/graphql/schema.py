'''Defines the GraphQL Queries and Mutations'''

import graphene
from pprint import pprint
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.rest_framework.serializer_converter import convert_serializer_to_input_type
from django.db import transaction
from rest_framework import serializers

from djangoAPI.models import *
from djangoAPI.apiUtils import *
from djangoAPI.graphql.asset_role_view import *
from djangoAPI.graphql.projects import *
from project.commons import *


# classes for outputs
class UnassAssViewType(DjangoObjectType):
    class Meta:
        model = UnassignedAssetsView


# class UnassAssViewTypeDeleted(graphene.ObjectType):
#     asset_serial_number = graphene.String()
#     id = graphene.Int()


class ReservationViewType(DjangoObjectType):
    class Meta:
        model = ReservationView


# Roundabout way to create fields for input in recon and asset view
# see https://github.com/graphql-python/graphene-django/issues/121

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


# unassigned asset mutations
class InsertUnassView(graphene.Mutation):
    class Arguments:
        objects = UnassViewSet(required=True)

    returning = graphene.List(UnassAssViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_serial_number': objects.asset_serial_number}
            data = MissingAssetUtil(data, auth)
            if data['result'] == 0:
                data = UnassignedAssetsView.objects.filter(
                    pk=data['errors'])
                return InsertUnassView(returning=data)
            raise GraphQLError(data['errors'])


class UpdateUnassView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = UnassViewSet(required=True)
    # TODO not sure what should be returned since the entry disappears
    returning = graphene.List(UnassAssViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'role_id': _set.role_id,
                    'asset_id': where.id._eq,
                    }
            result = list(UnassignedAssetsView.objects.filter(pk=where.id._eq))  # be optimistic
            # django orm queries are lazy (ie doesnt run until data is used) since data will no longer exist after we need to do something with it first
            # since we need to return a list with the object we deleted we can get the object before we delete it
            data = AssignAssetToRoleUtil(data, auth)
            if data['result'] == 0:
                return InsertUnassView(returning=result)
            raise GraphQLError(data['errors'])


class DeleteUnassView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
    # TODO not sure what should be returned since the entry disappears
    returning = graphene.List(UnassAssViewType)

    @staticmethod
    def mutate(root, info, where=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_id': where.id._eq, }
            result = list(UnassignedAssetsView.objects.filter(pk=where.id._eq))
            data = RetireAssetUtil(data, auth)
            if data['result'] == 0:
                return InsertUnassView(returning=result)  # same as above where list???
            raise GraphQLError(data['errors'])


class UpdateReserView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = ReserViewSet(required=True)
    returning = graphene.List(ReservationViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            if not _set.reserved is None:
                data = {'id': where.id._eq, 'reserved': _set.reserved}
                data = ReserveEntityUtil(data, auth)
            elif not _set.approved is None:
                data = {'id': where.id._eq, 'approved': _set.approved}
                data = ApproveReservationUtil(data, auth)
            else:
                raise GraphQLError('Unimplemented')
            if data['result'] == 0:
                data = ReservationView.objects.filter(
                    pk=data['errors'])
                return UpdateReserView(returning=data)
            raise GraphQLError(data['errors'])


class Query(ObjectType):
    user_projects = graphene.List(UsersProjectsType)
    project_details = graphene.List(ProjectDetailsType, project_id=graphene.Int())

    def resolve_user_projects(self, info, **kwargs):
        auth = AuthenticationUtil(info)
        return user_projects(auth['user_id'])

    def resolve_project_details(self, info, project_id):
        auth = AuthenticationUtil(info)
        return project_details('design', project_id)


class Mutations(graphene.ObjectType):
    insert_reconciliation_view = InsertReconciliationView.Field()
    update_reconciliation_view = UpdateReconView.Field()
    delete_reconciliation_view = DeleteReconView.Field()
    insert_unassigned_assets = InsertUnassView.Field()
    update_unassigned_assets = UpdateUnassView.Field()
    delete_unassigned_assets = DeleteUnassView.Field()
    update_reservation_view = UpdateReserView.Field()
    insert_orphan_view = InsertReconciliationView.Field()
    update_orphan_view = UpdateReconView.Field()
    delete_orphan_view = DeleteReconView.Field()
    insert_garbage_can_reconciliation_view = InsertReconciliationView.Field()
    update_garbage_can_reconciliation_view = UpdateReconView.Field()
    delete_garbage_can_reconciliation_view = DeleteReconView.Field()
    insert_garbage_can_unassigned_assets = InsertUnassView.Field()
    update_garbage_can_unassigned_assets = UpdateUnassView.Field()
    delete_garbage_can_unassigned_assets = DeleteUnassView.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
