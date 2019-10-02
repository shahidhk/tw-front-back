from django.db import models
from django.contrib.postgres import fields
from djangoAPI.value_lists import *
# Field.null default = False
# Field.blank default = False
# Field.choices used to limit values in a field, we will mostly use foreignkeys since it is easier to add an entry as opposed to changing python code
# Field.db_index 
# Field.default
# Field.primary_key django will auto create a primary key if non are set to primary key

# Project Tables
class projectTbl(models.Model):
    '''Master Table of Projects'''
    project_site = models.ForeignKey(operationalBusinessUnit, models.PROTECT)
    project_manager = models.CharField(max_length=400) # TODO this should be a foreign key?
    date_range = fields.DateRangeField()

class projectDesignPhaseTbl(models.Model):
    '''list all design phases'''
    project_tbl = models.ForeignKey(projectTbl, models.CASCADE)
    project_design_stage_type = models.ForeignKey(designStageTypeTbl, models.PROTECT) # TODO shouldnt this be a phase?
    planned_date_range = fields.DateRangeField()

class projectConstructionPhaseTbl(models.Model):
    '''list all construction stages'''
    project_tbl = models.ForeignKey(projectTbl, models.CASCADE)
    phase_number = models.BigIntegerField()
    planned_date_range = fields.DateRangeField()

class projectConstructionStageTbl(models.Model):
    '''list all contruction stages, stage is a subject of phase, daterange for stage must be within phase'''
    project_construction_phase = models.ForeignKey(projectConstructionPhaseTbl, models.CASCADE)
    project_construction_stage_type = models.ForeignKey(designStageTypeTbl, models.PROTECT)
    # TODO does there need to be a seperate list for construction stages?
    planned_date_range = fields.DateRangeField()

# Avantis Table
class clonedAssetAndRoleInRegistryTbl(models.Model):
    '''From Avantis'''
    mtnoi = models.AutoField(verbose_name="Avantis ID", primary_key=True)
    role_number = models.CharField(verbose_name="Entity Number", max_length=25, db_index=True, unique=True)
    role_name = models.CharField(verbose_name="Entity Name", max_length=200)
    parent_role_number = models.CharField(verbose_name="Parent Number", max_length=25, null=True, blank=True)
    role_location = models.CharField(verbose_name="Location", max_length=200, null=True, blank=True)
    role_criticality = models.BigIntegerField(verbose_name="Criticality Number", null=True, blank=True)
    role_priority = models.BigIntegerField(verbose_name="Priority Number", null=True, blank=True)
    role_equipment_type = models.CharField(verbose_name="Equipment Type", max_length=200, null=True, blank=True)
    role_classification = models.CharField(verbose_name="Classification", max_length=200, null=True, blank=True)
    asset_serial_number = models.CharField(verbose_name="Serial Number", max_length=300, null=True, blank=True)
    role_spatial_site_id = models.ForeignKey(importedSpatialSiteTbl, on_delete=models.PROTECT)
    suspension_id = models.BigIntegerField(null=True, blank=True)
    already_reserved = models.ForeignKey(projectTbl, models.SET_NULL, related_name='already_reserved_group', null=True, blank=True)
    intent_to_reserve = models.ForeignKey(projectTbl, models.SET_NULL, related_name='intent_reserve_group', null=True, blank=True)

    def __str__(self):
        return self.role_name

# Users & Authorization
class dbTbls(models.Model):
    # TODO figure out best way to impliment this
    # doesnt technically need auto updating since tables do not get created for projects
    db_table_name = models.CharField(max_length=400)

class userType(models.Model):
    user_type_name = models.CharField(max_length=400)
    tw_employee = models.BooleanField()
    city_employee = models.BooleanField()

class userTbl(models.Model):
    '''Master Table of Users'''
    username = models.CharField(max_length=400)
    user_type = models.ForeignKey(userType, models.PROTECT) # TODO how do the types relate to each other?
    organization_name = models.CharField(max_length=400) # should be a predefined list probably
    # TODO do we want email? for sending mail

class accessProfileTbl(models.Model):
    '''Master List of Avaliable User Access Profiles'''
    profile_name = models.CharField(max_length=400)

class userAccessLinkTbl(models.Model):
    '''Links Users with their Access Profiles'''
    user = models.ForeignKey(userTbl, models.CASCADE)
    profile = models.ForeignKey(accessProfileTbl, models.PROTECT)

class accessProfileDefinitionTbl(models.Model):
    profile = models.ForeignKey(accessProfileTbl, models.CASCADE)
    db_table = models.ForeignKey(dbTbls, models.PROTECT)
    view = models.BooleanField()
    update = models.BooleanField()
    add = models.BooleanField()
    delete = models.BooleanField()

class userProjectLinkTbl(models.Model):
    '''Links Users with their Projects'''
    user = models.ForeignKey(userTbl, models.CASCADE)
    project = models.ForeignKey(projectTbl, models.CASCADE)

# Role Tables
class projectAssetRoleRecordTbl(models.Model):
    '''Master List of all Roles'''
    parent_id = models.ForeignKey(to='self', to_field='id', verbose_name="Parent Number", on_delete=models.PROTECT, null=True, blank=True)
    updatable_role_number = models.CharField(max_length=25)
    role_name = models.CharField(max_length=400)
    role_spatial_site_id = models.ForeignKey(importedSpatialSiteTbl, models.PROTECT)
    role_criticality = models.ForeignKey(roleCriticality, models.PROTECT)
    role_priority = models.ForeignKey(rolePriority, models.PROTECT)
    project_tbl = models.ForeignKey(projectTbl, on_delete=models.PROTECT, null=True)

class preDesignReconciledRoleRecordTbl(projectAssetRoleRecordTbl):
    cloned_role_registry_tbl = models.ForeignKey(clonedAssetAndRoleInRegistryTbl, models.SET_NULL, null=True)
    entity_exists = models.BooleanField()
    missing_from_registry = models.BooleanField()
    designer_planned_action_type_tbl = models.ForeignKey(designerPlannedActionTypeTbl, models.PROTECT)

class newProjectAssetRoleTbl(projectAssetRoleRecordTbl):
    new_role = models.BooleanField()

# Asset Tables
class projectAssetRecordTbl(models.Model):
    '''Master Table of All Assets'''
    project_tbl = models.ForeignKey(projectTbl, on_delete=models.PROTECT, null=True)
    asset_serial_number = models.CharField(verbose_name="Serial Number", max_length=300, null=True, blank=True)

class preDesignReconciledAssetRecordTbl(projectAssetRecordTbl):
    '''Records What Errors Are Within Avantis'''
    cloned_role_registry_tbl = models.ForeignKey(clonedAssetAndRoleInRegistryTbl, models.SET_NULL, null=True)
    entity_exists = models.BooleanField()
    missing_from_registry = models.BooleanField()
    initial_project_asset_role_id = models.ForeignKey(projectAssetRoleRecordTbl, models.PROTECT, null=True) # link to the role the of asset
    designer_planned_action_type_tbl = models.ForeignKey(designerPlannedActionTypeTbl, models.PROTECT)

class existingAssetMovedByProjectTbl(preDesignReconciledAssetRecordTbl):
    '''Assets that will need to be moved to a new role'''
    final_project_asset_role_id = models.ForeignKey(projectAssetRoleRecordTbl, models.PROTECT)
    uninstallation_stage = models.ForeignKey(projectConstructionStageTbl, models.PROTECT, 'uninstall_stage')
    installation_stage = models.ForeignKey(projectConstructionStageTbl, models.PROTECT, 'install_stage')

class existingAssetDisposedByProjectTbl(preDesignReconciledAssetRecordTbl):
    '''Assets that will be removed'''
    uninstallation_stage = models.ForeignKey(projectConstructionStageTbl, models.PROTECT)

class newAssetDeliveredByProjectTbl(projectAssetRecordTbl):
    '''New Assets'''
    final_project_asset_role_id = models.ForeignKey(projectAssetRoleRecordTbl, models.PROTECT)
    installation_stage = models.ForeignKey(projectConstructionStageTbl, models.PROTECT)
