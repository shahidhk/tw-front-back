'''Module for defining Enum Models'''

from django.db import models
from djangoAPI.utils import num_to_alpha

# https://docs.hasura.io/1.0/graphql/manual/schema/enums.html#create-enum-table
# TODO https://docs.hasura.io/1.0/graphql/manual/api-reference/schema-metadata-api/table-view.html#set-table-is-enum


class DesignStageTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignStageTypeTbl'


class DesignProjectHumanRoleTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignProjectHumanRoleTypeTbl'


class ConstructionPhaseHumanRoleTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_ConstructionPhaseHumanRoleTypeTbl'


class ConstructionStageTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_ConstructionStageTypeTbl'


class DesignerPlannedActionTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignerPlannedActionTypeTbl'


class RoleCriticality(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_RoleCriticality'


class RolePriority(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_RolePriority'


class AccessProfileTbl(models.Model):
    '''Enum of Avaliable User Access Profiles'''
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_AccessProfileTbl'


class UserRole(models.Model):
    '''Enum of User Roles Avaliable'''
    id = models.CharField(primary_key=True, max_length=5)
    # use a, b, c...z, aa, ab
    role_title = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_UserRole'


def InitEnums():
    # there is probably a way to just iterate through all class in this module
    '''Initialize Enums with Test Values'''
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        DesignStageTypeTbl.objects.create(
            pk=i,
            name='Design Stage Type ' + str(i),
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        DesignProjectHumanRoleTypeTbl.objects.create(
            pk=i,
            name='Project Human Role Type ' + str(i),
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        ConstructionPhaseHumanRoleTypeTbl.objects.create(
            pk=i,
            name='Construction Phase Human Role Type ' + str(i),
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        ConstructionStageTypeTbl.objects.create(
            pk=i,
            name='Construction Stage Type ' + str(i),
        )
    for i, value in enumerate(['move', 'dispose', 'nothing']):
        DesignerPlannedActionTypeTbl.objects.create(
            pk=num_to_alpha(i),
            name=value,
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        RoleCriticality.objects.create(
            id=i,
            name='criticality ' + i,
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        RolePriority.objects.create(
            id=i,
            name='priority ' + i
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        AccessProfileTbl.objects.create(
            id=i,
            name='access profile ' + i
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        UserRole.objects.create(
            id=i,
            role_title='user role ' + i
        )
