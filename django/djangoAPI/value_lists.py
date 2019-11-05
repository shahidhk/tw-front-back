'''Module for Value Lists that aren't enums'''

from django.db import models
from djangoAPI.enum_models import *


class OperationalBusinessUnit(models.Model):
    '''Business Units'''
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'djangoAPI_OperationalBusinessUnit'


class Sites(models.Model):
    site_id = models.CharField(max_length=3)
    name = models.CharField(max_length=400)
    op_bus_unit = models.ForeignKey(OperationalBusinessUnit, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_Sites'


class DBTbls(models.Model):
    # TODO figure out best way to impliment this
    # doesnt technically need auto updating since tables do not get created for projects
    db_table_name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_DBTbls'


class UserType(models.Model):
    name = models.CharField(max_length=50)
    tw_employee = models.BooleanField()
    city_employee = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_UserType'


def InitValueList():
    # there is probably a way to just iterate through all class in this module
    '''Initialize ValueLists with Test Values'''
    for i in ['a', 'b', 'c', 'd']:
        OperationalBusinessUnit.objects.create(
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
    UserType.objects.create(
        id=1,
        name='a user',
        tw_employee=True,
        city_employee=True,
    )
