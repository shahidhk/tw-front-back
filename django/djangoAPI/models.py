from django.contrib.postgres import fields
from django.db import models

from djangoAPI.value_lists import *

# Field.null default = False
# Field.blank default = False
# Field.choices used to limit values in a field, we will mostly use foreignkeys since it is easier to add an entry as opposed to changing python code
# Field.db_index
# Field.default
# Field.primary_key django will auto create a primary key if non are set to primary key

# Project Tables


class ProjectTbl(models.Model):
    '''Master Table of Projects'''
    project_op_bus_unit = models.ForeignKey(
        OperationalBusinessUnit, models.PROTECT)
    design_contract_number = models.CharField(max_length=50)
    date_range = fields.DateRangeField()
    project_scope_description = models.TextField()

    class Meta:
        db_table = 'djangoAPI_ProjectTbl'


class ProjectDesignPhaseTbl(models.Model):
    '''list all design phases'''
    project_tbl = models.ForeignKey(ProjectTbl, models.CASCADE)
    project_design_stage_type = models.ForeignKey(
        DesignStageTypeTbl, models.PROTECT)
    # TODO shouldnt this be a phase?
    planned_date_range = fields.DateRangeField()

    class Meta:
        db_table = 'djangoAPI_ProjectDesignPhaseTbl'


class UserType(models.Model):
    user_type_name = models.CharField(max_length=400)
    tw_employee = models.BooleanField()
    city_employee = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_UserType'


class UserTbl(models.Model):
    '''Master Table of Users'''
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, models.PROTECT)
    organization_name = models.CharField(max_length=400)
    email = models.EmailField()

    class Meta:
        db_table = 'djangoAPI_UserTbl'


class ProjectConstructionPhaseTbl(models.Model):
    '''list all construction stages'''
    project_tbl = models.ForeignKey(ProjectTbl, models.CASCADE)
    phase_number = models.BigIntegerField()
    planned_date_range = fields.DateRangeField()
    manager = models.ForeignKey(UserTbl, models.PROTECT)
    description = models.TextField()

    class Meta:
        db_table = 'djangoAPI_ProjectConstructionPhaseTbl'


class ProjectConstructionStageTbl(models.Model):
    '''list all contruction stages, stage is a subject of phase, daterange for stage must be within phase'''
    project_construction_phase = models.ForeignKey(
        ProjectConstructionPhaseTbl, models.CASCADE)
    project_construction_stage_type = models.ForeignKey(
        DesignStageTypeTbl, models.PROTECT)
    # TODO does there need to be a seperate list for construction stages?
    planned_date_range = fields.DateRangeField()

    class Meta:
        db_table = 'djangoAPI_ProjectConstructionStageTbl'

# Avantis Table


class ClonedAssetAndRoleInRegistryTbl(models.Model):
    '''From Avantis'''
    mtoi = models.AutoField(verbose_name="Avantis ID", primary_key=True)
    role_number = models.CharField(
        verbose_name="Entity Number", max_length=25, db_index=True, unique=True)
    role_name = models.CharField(verbose_name="Entity Name", max_length=200)
    parent_role_number = models.CharField(
        verbose_name="Parent Number", max_length=25, null=True, blank=True)
    role_location = models.CharField(
        verbose_name="Location", max_length=200, null=True, blank=True)
    role_criticality = models.BigIntegerField(
        verbose_name="Criticality Number", null=True, blank=True)
    role_priority = models.BigIntegerField(
        verbose_name="Priority Number", null=True, blank=True)
    role_equipment_type = models.CharField(
        verbose_name="Equipment Type", max_length=200, null=True, blank=True)
    role_classification = models.CharField(
        verbose_name="Classification", max_length=200, null=True, blank=True)
    asset_serial_number = models.CharField(
        verbose_name="Serial Number", max_length=300, null=True, blank=True)
    role_spatial_site_id = models.ForeignKey(
        ImportedSpatialSiteTbl, on_delete=models.PROTECT)
    suspension_id = models.BigIntegerField(null=True, blank=True)
    already_reserved = models.ForeignKey(
        ProjectTbl, models.SET_NULL, related_name='already_reserved_group', null=True, blank=True)
    intent_to_reserve = models.ForeignKey(
        ProjectTbl, models.SET_NULL, related_name='intent_reserve_group', null=True, blank=True)

    class Meta:
        db_table = 'djangoAPI_ClonedAssetAndRoleInRegistryTbl'

    def __str__(self):
        return self.role_name

# Users & Authorization


class DBTbls(models.Model):
    # TODO figure out best way to impliment this
    # doesnt technically need auto updating since tables do not get created for projects
    db_table_name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_DBTbls'


class AccessProfileTbl(models.Model):
    '''Enum of Avaliable User Access Profiles'''
    id = models.CharField(primary_key=True, max_length=5)
    profile_name = models.CharField(max_length=400)

    class Meta:
        db_table = 'djangoAPI_AccessProfileTbl'


class UserAccessLinkTbl(models.Model):
    '''Links Users with their Access Profiles'''
    user = models.ForeignKey(UserTbl, models.CASCADE)
    profile = models.ForeignKey(AccessProfileTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_UserAccessLinkTbl'


class AccessProfileDefinitionTbl(models.Model):
    profile = models.ForeignKey(AccessProfileTbl, models.CASCADE)
    db_table = models.ForeignKey(DBTbls, models.PROTECT)
    view = models.BooleanField()
    update = models.BooleanField()
    add = models.BooleanField()
    delete = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_AccessProfileDefinitionTbl'


class UserRole(models.Model):
    '''Enum of User Roles Avaliable'''
    # https://docs.hasura.io/1.0/graphql/manual/schema/enums.html#create-enum-table
    # TODO https://docs.hasura.io/1.0/graphql/manual/api-reference/schema-metadata-api/table-view.html#set-table-is-enum
    id = models.CharField(
        primary_key=True, max_length=5)  # use a, b, c...z, aa, ab
    role_title = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_UserRole'


class UserProjectLinkTbl(models.Model):
    '''Links Users with their Projects'''
    user = models.ForeignKey(UserTbl, models.CASCADE)
    project = models.ForeignKey(ProjectTbl, models.CASCADE)
    title = models.ForeignKey(UserRole, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_UserProjectLinkTbl'

# Role Tables


class ProjectAssetRoleRecordTbl(models.Model):
    '''Master List of all Roles'''
    parent_id = models.ForeignKey(
        to='self', to_field='id', verbose_name="Parent Number", on_delete=models.PROTECT, null=True, blank=True)
    updatable_role_number = models.CharField(max_length=25)
    role_name = models.CharField(max_length=400)
    role_spatial_site_id = models.ForeignKey(
        ImportedSpatialSiteTbl, models.PROTECT)
    role_criticality = models.ForeignKey(RoleCriticality, models.PROTECT)
    role_priority = models.ForeignKey(RolePriority, models.PROTECT)
    project_tbl = models.ForeignKey(
        ProjectTbl, on_delete=models.PROTECT, null=True)
    approved = models.BooleanField(default=False)
    # to impliment ltree, since the type isnt correctly this table will be unmanaged
    ltree_path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djangoAPI_ProjectAssetRoleRecordTbl'


class PreDesignReconciledRoleRecordTbl(ProjectAssetRoleRecordTbl):
    cloned_role_registry_tbl = models.ForeignKey(
        ClonedAssetAndRoleInRegistryTbl, models.SET_NULL, null=True)
    entity_exists = models.BooleanField()
    missing_from_registry = models.BooleanField()
    designer_planned_action_type_tbl = models.ForeignKey(
        DesignerPlannedActionTypeTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_PreDesignReconciledRoleRecordTbl'


class NewProjectAssetRoleTbl(ProjectAssetRoleRecordTbl):
    new_role = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_NewProjectAssetRoleTbl'

# Asset Tables


class ProjectAssetRecordTbl(models.Model):
    '''Master Table of All Assets'''
    project_tbl = models.ForeignKey(
        ProjectTbl, on_delete=models.PROTECT, null=True)
    asset_serial_number = models.CharField(
        verbose_name="Serial Number", max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'djangoAPI_ProjectAssetRecordTbl'


class AssetClassificationTbl(models.Model):
    '''List of all Classifications given to an asset'''
    asset = models.ForeignKey(ProjectAssetRecordTbl, models.CASCADE)
    # TODO should there be an acceptable list of classifications?
    classification = models.TextField()

    class Meta:
        db_table = 'djangoAPI_AssetClassificationTbl'


class PreDesignReconciledAssetRecordTbl(ProjectAssetRecordTbl):
    '''Records What Errors Are Within Avantis'''
    cloned_role_registry_tbl = models.ForeignKey(
        ClonedAssetAndRoleInRegistryTbl, models.SET_NULL, null=True)
    entity_exists = models.BooleanField()
    missing_from_registry = models.BooleanField()
    initial_project_asset_role_id = models.ForeignKey(
        ProjectAssetRoleRecordTbl, models.PROTECT, null=True)  # link to the role the of asset
    designer_planned_action_type_tbl = models.ForeignKey(
        DesignerPlannedActionTypeTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_PreDesignReconciledAssetRecordTbl'


class ExistingAssetMovedByProjectTbl(PreDesignReconciledAssetRecordTbl):
    '''Assets that will need to be moved to a new role'''
    final_project_asset_role_id = models.ForeignKey(
        ProjectAssetRoleRecordTbl, models.PROTECT)
    uninstallation_stage = models.ForeignKey(
        ProjectConstructionStageTbl, models.PROTECT, 'uninstall_stage')
    installation_stage = models.ForeignKey(
        ProjectConstructionStageTbl, models.PROTECT, 'install_stage')

    class Meta:
        db_table = 'djangoAPI_ExistingAssetMovedByProjectTbl'


class ExistingAssetDisposedByProjectTbl(PreDesignReconciledAssetRecordTbl):
    '''Assets that will be removed'''
    uninstallation_stage = models.ForeignKey(
        ProjectConstructionStageTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_ExistingAssetDisposedByProjectTbl'


class NewAssetDeliveredByProjectTbl(ProjectAssetRecordTbl):
    '''New Assets'''
    final_project_asset_role_id = models.ForeignKey(
        ProjectAssetRoleRecordTbl, models.PROTECT)
    installation_stage = models.ForeignKey(
        ProjectConstructionStageTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_NewAssetDeliveredByProjectTbl'


class ReconciliationView(models.Model):
    '''Read only model using data from reconciliation_view'''
    id = models.IntegerField(primary_key=True)
    role_number = models.TextField(null=True)
    role_name = models.TextField(null=True)
    # TODO try setting this to a FK to get a relation
    parent = models.IntegerField(null=True)
    project_id = models.IntegerField(null=True)
    role_exists = models.BooleanField(null=True)
    role_missing_from_registry = models.BooleanField(null=True)
    full_path = models.TextField(null=True)
    asset_id = models.IntegerField(null=True)
    asset_serial_number = models.TextField(null=True)
    asset_exists = models.BooleanField(null=True)
    asset_missing_from_registry = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = "reconciliation_view"


class UnassignedAssetsView(models.Model):
    '''Read Only model using data from unassigned_assets'''
    # TODO this probably does not need to be a view, a filter probably works
    id = models.IntegerField(primary_key=True)
    asset_serial_number = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "unassigned_assets"
