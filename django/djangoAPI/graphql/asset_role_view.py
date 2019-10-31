import graphene
from django.db import transaction
from graphene_django.rest_framework.serializer_converter import \
    convert_serializer_to_input_type
from graphene_django.types import DjangoObjectType, ObjectType
from graphql import GraphQLError
from rest_framework import serializers

from djangoAPI.apiUtils import *
from djangoAPI.graphql.commons import *
from djangoAPI.models import *


# output classes
class ReconViewType(DjangoObjectType):
    class Meta:
        model = ReconciliationView


# input classes
class ReconViewSerial(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationView
        # the id is excluded since the client will never be able to specify the primary key, it will be returned once the entry is generated on the db
        exclude = ('id',)


class ReconciliationViewSet(convert_serializer_to_input_type(ReconViewSerial)):
    role_id = graphene.Int()


# mutations
class InsertReconciliationView(graphene.Mutation):
    class Arguments:
        objects = ReconciliationViewSet(required=True)

    returning = graphene.List(ReconViewType)

    @staticmethod
    def mutate(root, info, objects=None):
        auth = AuthenticationUtil(info)
        if not auth['valid']:
            raise GraphQLError('User / Client is not properly authenticated. Please Login.')
        role_data = {
            'role_number': objects.role_number,
            'role_spatial_site_id': 1,  # objects.role_spatial_site_id
            'role_priority': 'a',  # objects.role_priority
            'role_name': objects.role_name,
            'role_criticality': 'a',  # objects.role_criticality
            'parent_id': objects.parent,
        }
        new_entity = MissingRoleUtil(role_data, auth)
        if new_entity['result'] == 0:
            new_entity = ReconciliationView.objects.filter(
                pk=new_entity['errors'])
            return InsertReconciliationView(returning=new_entity)
        raise GraphQLError(new_entity['errors'])


class UpdateReconView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)
        _set = ReconciliationViewSet(required=True)

    returning = graphene.List(ReconViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        with transaction.atomic():
            # call different functions depending on what is changed
            # TODO allow changing multiple columns at the same time
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            if not _set.role_exists is None:
                # marks role and asset as does not exist / deletes user created
                data = {'role_id': where.id._eq,
                        'entity_exists': _set.role_exists,
                        }
                data = remove_reconciliation(data, auth)
            elif not _set.parent is None:
                data = {'role_id': where.id._eq,
                        'parent_id': _set.parent,
                        }
                data = RoleParentUtil(data, auth)
            elif not _set.asset_id is None:
                # this one is kinda weird, assigns an asset to the role,
                # if moving asset to unassigned assets, the role_id is 0 / None
                data = {'role_id': where.id._eq,
                        'asset_id': _set.asset_id,
                        }
                data = AssignAssetToRoleUtil(data, auth)
            else:
                raise GraphQLError('Unimplemented')
            # Check the result of called function and return row on success
            if data['result'] == 0:
                data = ReconciliationView.fixed_ltree(pk=data['errors'])
                return UpdateReconView(returning=data)
            raise GraphQLError(data['errors'])


class DeleteReconView(graphene.Mutation):
    class Arguments:
        where = IDEQ(required=True)

    returning = graphene.List(ReconViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        with transaction.atomic():
            auth = AuthenticationUtil(info)
            if not auth['valid']:
                raise GraphQLError('User / Client is not properly authenticated. Please Login.')
            data = {'role_id': where.id._eq, 'entity_exists': False, }
            result = ReconciliationView.fixed_ltree(pk=where.id._eq)
            data = remove_reconciliation(data, auth)
            if data['result'] == 0:
                data = ReconciliationView.fixed_ltree(pk=data['errors'])
                return UpdateReconView(returning=(data if data else result))
            raise GraphQLError(data['errors'])


class UpdateOrphanView(graphene.Mutation):
    # Reservation and Orphan View are based on the same table so they can have the same inputs & outputs
    class Arguments:
        where = IDEQ(required=True)
        _set = ReconciliationViewSet(required=True)
    returning = graphene.List(ReconViewType)

    @staticmethod
    def mutate(root, info, where=None, _set=None):
        auth = AuthenticationUtil(info)
        if not auth['valid']:
            raise GraphQLError('User / Client is not properly authenticated. Please Login.')
        if not _set.parent is None:
            # Used to assign orphaned child to a new parent, drags from orphan_view to reconciliation view
            data = {'role_id': where.id._eq, 'parent_id': _set.parent}
            data = RoleParentUtil(data, auth)
        if data['result'] == 0:
            data = ReconciliationView.fixed_ltree(pk=data['errors'])
            return UpdateOrphanView(returning=data)
        raise GraphQLError(data['errors'])
