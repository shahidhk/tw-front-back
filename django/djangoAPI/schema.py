import graphene

from graphene_django.types import DjangoObjectType, ObjectType

from djangoAPI.models import *


class AvantisType(DjangoObjectType):
    class Meta:
        model = ClonedAssetAndRoleInRegistryTbl
        # fields = ('importedspatialsitetbl',)


class ImportedSpatialSiteTblType(DjangoObjectType):
    class Meta:
        model = ImportedSpatialSiteTbl


class Query(ObjectType):
    all_sites = graphene.List(ImportedSpatialSiteTblType)
    all_avantis = graphene.List(AvantisType)


schema = graphene.Schema(query=Query)
