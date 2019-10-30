from django.contrib.postgres import fields
from django.db import models

from djangoAPI.value_lists import *
from djangoAPI.enum_models import *
from djangoAPI.utils import *

# Field.null default = False
# Field.blank default = False
# Field.choices used to limit values in a field, we will mostly use foreignkeys since it is easier to add an entry as opposed to changing python code
# Field.db_index
# Field.default
# Field.primary_key django will auto create a primary key if non are set to primary key


class UserTbl(models.Model):
    '''Master Table of Users'''
    # TODO WIP
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, models.PROTECT)
    organization_name = models.CharField(max_length=400)
    email = models.EmailField()

    class Meta:
        db_table = 'djangoAPI_UserTbl'

# Project Tables


class SuperDesignProjectTbl(models.Model):
    '''Super set of design projects'''
    # TODO Consider dropping 'super' projectset, projectgroup
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'djangoAPI_SuperDesignProjectTbl'


class DesignProjectTbl(models.Model):
    '''Table of Design Projects
    If a design project requires construction
    it will be linked to this table'''
    name = models.CharField(max_length=100)
    super_design_project = models.ForeignKey(
        SuperDesignProjectTbl, models.PROTECT, blank=True, null=True)
    phase_number = models.IntegerField(blank=True, null=True)
    op_bus_unit = models.ForeignKey(OperationalBusinessUnit, models.PROTECT)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    planned_date_range = fields.DateRangeField(blank=True, null=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    # TODO limited to 999B
    scope_description = models.TextField(blank=True, null=True)
    # TODO not in sqldbm but there needs to be a project scope description

    class Meta:
        db_table = 'djangoAPI_DesignProjectTbl'


class DesignProjectHumanRoleTbl(models.Model):
    '''Users Related to the project'''
    user_id = models.ForeignKey(UserTbl, models.PROTECT)
    design_project = models.ForeignKey(DesignProjectTbl, models.PROTECT)
    human_role_type = models.ForeignKey(DesignProjectHumanRoleTypeTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_DesignProjectHumanRoleTbl'


class DesignStageTbl(models.Model):
    '''list all design phases'''
    design_project = models.ForeignKey(DesignProjectTbl, models.CASCADE)
    design_stage_type = models.ForeignKey(DesignStageTypeTbl, models.PROTECT)
    planned_date_range = fields.DateRangeField()

    class Meta:
        db_table = 'djangoAPI_DesignPhaseTbl'


class ConstructionPhaseTbl(models.Model):
    '''list all construction stages'''
    name = models.CharField(max_length=200)
    design_project = models.ForeignKey(DesignProjectTbl, models.SET_NULL, blank=True, null=True)
    phase_number = models.BigIntegerField(blank=True, null=True)
    op_bus_unit = models.ForeignKey(OperationalBusinessUnit, models.PROTECT)
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    planned_date_range = fields.DateRangeField(blank=True, null=True)
    scope_description = models.TextField()
    # TODO same concerns as designprojecttbl

    class Meta:
        db_table = 'djangoAPI_ConstructionPhaseTbl'


class ConstructionPhaseHumanRoleTbl(models.Model):
    user_id = models.ForeignKey(UserTbl, models.PROTECT)
    construction_phase = models.ForeignKey(ConstructionPhaseTbl, models.PROTECT)
    human_role_type = models.ForeignKey(ConstructionPhaseHumanRoleTypeTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_ConstructionPhaseHumanRoleTbl'


class ConstructionStageTbl(models.Model):
    '''list all contruction stages, stage is a subject of phase, daterange for stage must be within phase'''
    construction_phase = models.ForeignKey(ConstructionPhaseTbl, models.CASCADE)
    construction_stage_type = models.ForeignKey(ConstructionStageTypeTbl, models.PROTECT)
    planned_date_range = fields.DateRangeField()

    class Meta:
        db_table = 'djangoAPI_ConstructionStageTbl'

# Avantis Table


class ImportedSpatialSiteTbl(models.Model):
    spatial_site_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=400)
    parent_site_id = models.ForeignKey(
        to='self', to_field='spatial_site_id', on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'djangoAPI_ImportedSpatialSiteTbl'


class ClonedAssetAndRoleInRegistryTbl(models.Model):
    '''From Avantis'''
    mtoi = models.AutoField(verbose_name="Avantis ID", primary_key=True)
    role_number = models.CharField(
        verbose_name="Entity Number", max_length=25, db_index=True, unique=True)
    role_name = models.CharField(verbose_name="Entity Name", max_length=200)
    parent_role_number = models.CharField(
        verbose_name="Parent Number", max_length=25, null=True, blank=True)
    # TODO bad practise to allow nulls for strings (default is empty string)
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
    role_spatial_site_id = models.ForeignKey(ImportedSpatialSiteTbl, on_delete=models.PROTECT)
    suspension_id = models.BigIntegerField(null=True, blank=True)
    already_reserved = models.ForeignKey(
        DesignProjectTbl, models.SET_NULL, related_name='already_reserved_group', null=True, blank=True)
    intent_to_reserve = models.ForeignKey(
        DesignProjectTbl, models.SET_NULL, related_name='intent_reserve_group', null=True, blank=True)

    class Meta:
        db_table = 'djangoAPI_ClonedAssetAndRoleInRegistryTbl'

    def __str__(self):
        return self.role_name


class AvantisAdditions(ClonedAssetAndRoleInRegistryTbl):
    '''Additional processed fields to add data to the avantis table'''
    parent_mtoi = models.ForeignKey(
        to='self', on_delete=models.SET_NULL, null=True)
    # role_spatial_site_id = models.ForeignKey(ImportedSpatialSiteTbl, on_delete=models.PROTECT)
    full_path = models.TextField()

    class Meta:
        db_table = 'djangoAPI_AvantisAdditions'
        managed = False

# Users & Authorization


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


class UserProjectLinkTbl(models.Model):
    '''Links Users with their Projects'''
    user = models.ForeignKey(UserTbl, models.CASCADE)
    project = models.ForeignKey(DesignProjectTbl, models.CASCADE)
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
    role_spatial_site_id = models.ForeignKey(ImportedSpatialSiteTbl, models.PROTECT)
    role_criticality = models.ForeignKey(RoleCriticality, models.PROTECT)
    role_priority = models.ForeignKey(RolePriority, models.PROTECT)
    project_tbl = models.ForeignKey(DesignProjectTbl, on_delete=models.PROTECT, null=True)
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
    parent_changed = models.BooleanField()

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
        DesignProjectTbl, on_delete=models.PROTECT, null=True)
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
    role_changed = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_PreDesignReconciledAssetRecordTbl'


class ExistingAssetMovedByProjectTbl(PreDesignReconciledAssetRecordTbl):
    '''Assets that will need to be moved to a new role'''
    final_project_asset_role_id = models.ForeignKey(
        ProjectAssetRoleRecordTbl, models.PROTECT)
    uninstallation_stage = models.ForeignKey(
        ConstructionStageTbl, models.PROTECT, 'uninstall_stage')
    installation_stage = models.ForeignKey(
        ConstructionStageTbl, models.PROTECT, 'install_stage')

    class Meta:
        db_table = 'djangoAPI_ExistingAssetMovedByProjectTbl'


class ExistingAssetDisposedByProjectTbl(PreDesignReconciledAssetRecordTbl):
    '''Assets that will be removed'''
    uninstallation_stage = models.ForeignKey(
        ConstructionStageTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_ExistingAssetDisposedByProjectTbl'


class NewAssetDeliveredByProjectTbl(ProjectAssetRecordTbl):
    '''New Assets'''
    final_project_asset_role_id = models.ForeignKey(
        ProjectAssetRoleRecordTbl, models.PROTECT)
    installation_stage = models.ForeignKey(
        ConstructionStageTbl, models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_NewAssetDeliveredByProjectTbl'


# Views
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
    parent_changed = models.BooleanField(null=True)
    asset_id = models.IntegerField(null=True)
    asset_serial_number = models.TextField(null=True)
    asset_exists = models.BooleanField(null=True)
    asset_missing_from_registry = models.BooleanField(null=True)
    role_changed = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = "reconciliation_view_temp"

    @staticmethod
    def fixed_ltree(pk):
        '''retrives list of objects with fixed ltree'''
        lst = list(ReconciliationView.objects.filter(pk=pk))
        for l in lst:
            i = l.full_path.index('.')
            l.full_path = l.full_path[i+1:]
        return lst


class UnassignedAssetsView(models.Model):
    '''Read Only model using data from unassigned_assets'''
    # TODO this probably does not need to be a view, a filter probably works
    id = models.IntegerField(primary_key=True)
    asset_serial_number = models.TextField(null=True)

    class Meta:
        managed = False
        db_table = "unassigned_assets"


class ReservationView(models.Model):
    '''Read only model using data from reservation_view'''
    id = models.IntegerField(primary_key=True)
    role_number = models.TextField(null=True)
    role_name = models.TextField(null=True)
    parent = models.IntegerField(null=True)
    project_id = models.IntegerField(null=True)
    full_path = models.TextField(null=True)
    approved = models.BooleanField(null=True)
    reserved = models.BooleanField(null=True)
    approval_status = models.TextField(null=True)
    reservable = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = "reservation_view"

    def change_reservation(self, project_id, reserve):
        """Updates reservation project ids for assets & roles"""
        key = self.pk
        try:
            asset = ProjectAssetRecordTbl.objects.get(predesignreconciledassetrecordtbl__cloned_role_registry_tbl=key)
            role = ProjectAssetRoleRecordTbl.objects.get(predesignreconciledrolerecordtbl__cloned_role_registry_tbl=key)
        except Exception as e:
            return Result(success=False, message='Cannot find corresponding asset, are you sure this is an Avantis Asset?', exception=e, error_code=1)
        if asset.project_tbl != role.project_tbl:
            return Result(success=False, message='DB inconsistency error asset and role reserved by different projects. Please Contact Tony Huang', exception=e, error_code=2)
        if asset.project_tbl is None:  # asset is free real estate
            if reserve:
                asset.project_tbl_id = project_id
                role.project_tbl_id = project_id
            else:  # dont return error if already unreserved
                return Result(success=True, obj_id=key)
        elif asset.project_tbl_id == project_id:  # asset is reserved by this group
            if not reserve:  # when reserved=False they are trying to unreserve
                asset.project_tbl = None
                role.project_tbl = None
                role.approved = False
            else:  # dont return error if already reserved
                return Result(success=True, obj_id=key)
        else:  # asset is reserved by another group
            return Result(success=False, message='Asset is reserved by another project group', error_code=3)
        try:
            asset.save()
            role.save()
        except Exception as e:
            return Result(success=False, message='Cannot change reservation', exception=e, error_code=4)
        else:
            return Result(success=True, obj_id=key)