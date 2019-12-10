import graphene
from django.db import transaction
from graphene_django.rest_framework.serializer_converter import \
    convert_serializer_to_input_type
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from rest_framework import serializers

from djangoAPI.apiUtils import (AuthenticationUtil, MissingAssetUtil,
                                RetireAssetUtil, assign_asset_to_role_change,
                                assign_asset_to_role_reconciliation,
                                remove_asset)
from djangoAPI.graphql.commons import IDEQ
from djangoAPI.models import (NewAssetDeliveredByProjectTbl,
                              UnassignedAssetsView)

# outputs


class UnassignedAssetViewType(DjangoObjectType):
    class Meta:
        model = UnassignedAssetsView

# inputs


class UnassignedAssetViewSerial(serializers.ModelSerializer):
    class Meta:
        model = UnassignedAssetsView
        exclude = ('id',)


class UnassignedAssetViewSet(convert_serializer_to_input_type(UnassignedAssetViewSerial)):
    role_id = graphene.Int()
    id = graphene.Int()


# mutation
class InsertReconciliationUnassignedAssetView(graphene.Mutation):
    class Arguments:
        objects = UnassignedAssetViewSet(required=True)

    returning = graphene.List(UnassignedAssetViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_serial_number': objects.asset_serial_number}
            data = MissingAssetUtil(data, auth)
            if data['result'] == 0:
                data = list(UnassignedAssetsView.objects.filter(
                    pk=data['errors']))
                return InsertReconciliationUnassignedAssetView(returning=data)
            raise GraphQLError(data['errors'])


class UpdateReconciliationUnassignedAssetView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = UnassignedAssetViewSet(required=True)
    returning = graphene.List(UnassignedAssetViewType)

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
            data = assign_asset_to_role_reconciliation(data, auth)
            if data.success:
                return UpdateReconciliationUnassignedAssetView(returning=result)
            raise GraphQLError(data.readable_message())


class DeleteReconciliationUnassignedAssetView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
    returning = graphene.List(UnassignedAssetViewType)

    @staticmethod
    def mutate(root, info, where=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_id': where.id._eq, }
            result = list(UnassignedAssetsView.objects.filter(pk=where.id._eq))
            data = RetireAssetUtil(data, auth)
            if data.success:
                return DeleteReconciliationUnassignedAssetView(returning=result)
            raise GraphQLError(data.readable_message())


class InsertChangeUnassignedAssetView(graphene.Mutation):
    class Arguments:
        objects = UnassignedAssetViewSet(required=True)

    returning = graphene.List(UnassignedAssetViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_serial_number': objects.asset_serial_number}
            data = NewAssetDeliveredByProjectTbl.add(data, auth['group'], None)
            if data.success:
                data = list(UnassignedAssetsView.objects.filter(pk=data.obj_id))
                return InsertChangeUnassignedAssetView(returning=data)
            raise GraphQLError(data.readable_message())


class UpdateChangeUnassignedAssetView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = UnassignedAssetViewSet(required=True)
    returning = graphene.List(UnassignedAssetViewType)

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
            data = assign_asset_to_role_change(data, auth)
            if data.success:
                return UpdateChangeUnassignedAssetView(returning=result)
            raise GraphQLError(data.readable_message())


class DeleteChangeUnassignedAssetView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
    returning = graphene.List(UnassignedAssetViewType)

    @staticmethod
    def mutate(root, info, where=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'asset_id': where.id._eq, }
            result = list(UnassignedAssetsView.objects.filter(pk=where.id._eq))
            data = remove_asset(data, auth)
            if data.success:
                return DeleteChangeUnassignedAssetView(returning=result)
            raise GraphQLError(data.readable_message())
