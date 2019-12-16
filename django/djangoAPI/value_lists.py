'''Module for Value Lists and Enums'''

from django.db import models
from djangoAPI.utils import num_to_alpha
from django.apps import apps


class BusinessUnit(models.Model):
    '''Business Units'''
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_BusinessUnit'


class Sites(models.Model):
    site_id = models.CharField(max_length=3)
    name = models.CharField(max_length=400)
    op_bus_unit = models.ForeignKey(BusinessUnit, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_Sites'


class DBTbls(models.Model):
    db_table_name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_DBTbls'


class UserType(models.Model):
    name = models.CharField(max_length=50)
    tw_employee = models.BooleanField()
    city_employee = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_UserType'


class AllHumanRoleTypeTbl(models.Model):
    id = models.TextField(primary_key=True)

    class Meta:
        db_table = 'djangoAPI_AllHumanRoleTypeTbl'


class SystemHumanRoleTypeTbl(models.Model):
    id = models.OneToOneField(to=AllHumanRoleTypeTbl, on_delete=models.PROTECT, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_SystemHumanRoleTypeTbl'


class DesignStageTypeTbl(models.Model):
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignStageTypeTbl'


class DesignProjectHumanRoleTypeTbl(models.Model):
    id = models.OneToOneField(to=AllHumanRoleTypeTbl, on_delete=models.PROTECT, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignProjectHumanRoleTypeTbl'


class ConstructionPhaseHumanRoleTypeTbl(models.Model):
    id = models.OneToOneField(to=AllHumanRoleTypeTbl, on_delete=models.PROTECT, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_ConstructionPhaseHumanRoleTypeTbl'


class ConstructionStageTypeTbl(models.Model):
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_ConstructionStageTypeTbl'


class DesignerPlannedActionTypeTbl(models.Model):
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_DesignerPlannedActionTypeTbl'


class RoleCriticality(models.Model):
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_RoleCriticality'


class RolePriority(models.Model):
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_RolePriority'


class AccessProfileTbl(models.Model):
    '''Enum of Avaliable User Access Profiles'''
    id = models.TextField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_AccessProfileTbl'


class UserRole(models.Model):
    '''Enum of User Roles Avaliable'''
    # TODO check if unused
    id = models.TextField(primary_key=True, max_length=5)
    role_title = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_UserRole'


class UserGroupNameTbl(models.Model):
    """
    User group??
    """
    name = models.CharField(max_length=20)
    within_city = models.BooleanField()
    with_toronto_water = models.BooleanField()
    outside_organization_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'djangoAPI_UserGroupNameTbl'


def init_value_lists():
    # there is probably a way to just iterate through all class in this module
    """Initialize Enums with Test Values"""
    for i in ['a', 'b', 'c', 'd']:
        BusinessUnit.objects.create(
            pk=i,
            name='OpBusUnit ' + str(i),
        )
    for i, value in enumerate(['a', 'b', 'c', 'd', 'e', 'f']):
        Sites.objects.create(
            pk=i+1,
            site_id=value,
            name='site ' + value,
            op_bus_unit_id=['a', 'b', 'c', 'd', 'e', 'f'][int((i)/2)]
        )
    all_models = apps.get_models()
    for model in all_models:
        if model._meta.app_label == 'djangoAPI':
            DBTbls.objects.create(
                db_table_name=model._meta.db_table
            )
    UserType.objects.create(
        id=1,
        name='a user',
        tw_employee=True,
        city_employee=True,
    )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        AllHumanRoleTypeTbl.objects.create(
            id=i
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        SystemHumanRoleTypeTbl.objects.create(
            pk=i,
            name='System Human Role Type ' + str(i),
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        DesignStageTypeTbl.objects.create(
            pk=i,
            name='Design Stage Type ' + str(i),
        )
    for i in ['a', 'b', 'c', 'd', 'e', 'f']:
        people = {'b': 'Project Manager', 'c': 'Key Business Unit Contact', 'd': 'Asset Data Steward'}
        DesignProjectHumanRoleTypeTbl.objects.create(
            pk=i,
            name=people.get(i, 'Design Project Human Role Type ' + str(i)),
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
            pk=num_to_alpha(i+1),
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
    for i, value in enumerate(['a', 'b', 'c', 'd', 'e', 'f']):
        obj = UserGroupNameTbl.objects.create(
            name='user group id '+value,
            within_city=True,
            with_toronto_water=True,
        )
        obj.pk = i + 1
        obj.save()
