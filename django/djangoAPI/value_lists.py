from django.db import models


class OperationalBusinessUnit(models.Model):
    '''Enum Business Units'''
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_OperationalBusinessUnit'


class Sites(models.Model):
    site_id = models.CharField(max_length=3)
    site_name = models.CharField(max_length=400)
    op_bus_unit = models.ForeignKey(OperationalBusinessUnit, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_Sites'


class DesignStageTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_DesignStageTypeTbl'


class DesignerPlannedActionTypeTbl(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_DesignerPlannedActionTypeTbl'


class ImportedSpatialSiteTbl(models.Model):
    spatial_site_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400)
    parent_site_id = models.ForeignKey(
        to='self', to_field='spatial_site_id', on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'djangoAPI_ImportedSpatialSiteTbl'


class RoleCriticality(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_RoleCriticality'


class RolePriority(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_RolePriority'
