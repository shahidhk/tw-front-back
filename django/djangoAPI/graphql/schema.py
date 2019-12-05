'''Defines the GraphQL Queries and Mutations'''

import graphene
from django.db import transaction
from graphene_django.rest_framework.serializer_converter import \
    convert_serializer_to_input_type
from graphene_django.types import DjangoObjectType, ObjectType
from graphql import GraphQLError
from rest_framework import serializers

from djangoAPI.apiUtils import (ApproveReservationUtil, AuthenticationUtil,
                                ReserveEntityUtil)
from djangoAPI.graphql.asset_role_view import (DeleteChangeView,
                                               DeleteReconciliationView,
                                               InsertChangeView,
                                               InsertReconciliationView,
                                               UpdateChangeView,
                                               UpdateReconciliationView)
from djangoAPI.graphql.commons import IDEQ, QueryTypeCache, TableType
from djangoAPI.graphql.projects import ProjectDetailsType, UsersProjectsType
from djangoAPI.graphql.unassigned_asset_view import (
    DeleteReconciliationUnassignedAssetView, InsertReconciliationUnassignedAssetView,
    UpdateReconciliationUnassignedAssetView)
from djangoAPI.models import ReservationView
from project.commons import ProjectDetails, project_details, user_projects


# classes for outputs
class ReservationViewType(DjangoObjectType):
    class Meta:
        model = ReservationView


# Roundabout way to create fields for inputs
# see https://github.com/graphql-python/graphene-django/issues/121
class ReservationViewSerial(serializers.ModelSerializer):
    class Meta:
        model = ReservationView
        exclude = ('id',)


class ReserViewSet(convert_serializer_to_input_type(ReservationViewSerial)):
    pass


# mutations
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
    project_details = graphene.List(ProjectDetailsType, where=IDEQ(
        required=False))  # default is false btw
    get_type_name = graphene.Field(TableType, name=graphene.String(required=True))

    def resolve_user_projects(self, info, **kwargs):
        auth = AuthenticationUtil(info)
        return user_projects(auth['user_id'])

    def resolve_project_details(self, info, where=None):
        if not where:
            return [ProjectDetails()]
        auth = AuthenticationUtil(info)
        return [project_details(where.id._eq)]

    def resolve_get_type_name(self, info, name='', **kwargs):
        try:
            cache = QueryTypeCache.objects.get(name=name)
        except QueryTypeCache.DoesNotExist:
            cache = QueryTypeCache.update(name=name)
        return cache


class Mutations(graphene.ObjectType):
    update_reservation_view = UpdateReserView.Field()

    insert_reconciliation_view = InsertReconciliationView.Field()
    update_reconciliation_view = UpdateReconciliationView.Field()
    delete_reconciliation_view = DeleteReconciliationView.Field()
    update_reconciliation_orphan_view = UpdateReconciliationView.Field()
    delete_reconciliation_orphan_view = DeleteReconciliationView.Field()
    update_garbage_can_reconciliation_view = UpdateReconciliationView.Field()

    insert_reconciliation_unassigned_asset_view = InsertReconciliationUnassignedAssetView.Field()
    update_reconciliation_unassigned_asset_view = UpdateReconciliationUnassignedAssetView.Field()
    delete_reconciliation_unassigned_asset_view = DeleteReconciliationUnassignedAssetView.Field()
    update_garbage_can_asset_view = UpdateReconciliationUnassignedAssetView.Field()

    insert_change_view = InsertChangeView.Field()
    update_change_view = UpdateChangeView.Field()
    delete_change_view = DeleteChangeView.Field()
    update_dumpster_change_view = UpdateChangeView.Field()

    # changed unassigned asset views


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
