from django.db import models

class operationalBusinessUnit(models.Model):
    name = models.CharField(max_length=400)

class sites(models.Model):
    site_id = models.CharField(max_length=3)
    site_name = models.CharField(max_length=400)
    op_bus_unit = models.ForeignKey(operationalBusinessUnit, models.PROTECT)

class designStageTypeTbl(models.Model):
    name = models.CharField(max_length=400)

class designerPlannedActionTypeTbl(models.Model):
    name = models.CharField(max_length=400)

class importedSpatialSiteTbl(models.Model):
    spatialSiteID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400)
    parentSiteId = models.ForeignKey(to='self', to_field='spatialSiteID', on_delete=models.PROTECT, null=True)

class roleCriticality(models.Model):
    id = models.AutoField(primary_key=True)

class rolePriority(models.Model):
    id = models.AutoField(primary_key=True)