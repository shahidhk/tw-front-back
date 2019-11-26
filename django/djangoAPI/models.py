from django.contrib.auth.models import User
from django.contrib.postgres import fields
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from djangoAPI.utils import *
from djangoAPI.value_lists import *

# Field.null default = False
# Field.blank default = False
# Field.choices used to limit values in a field, we will mostly use foreignkeys since it is easier to add an entry as opposed to changing python code
# Field.db_index
# Field.default
# Field.primary_key django will auto create a primary key if non are set to primary key


class UserTbl(models.Model):
    '''Master Table of Users'''
    # use built in user module for first/last name, username and email
    auth_user = models.OneToOneField(to=User, on_delete=models.PROTECT, primary_key=True)
    role = models.ForeignKey(SystemHumanRoleTypeTbl, models.PROTECT)
    user_group_name = models.ForeignKey(to=UserGroupNameTbl, on_delete=models.PROTECT)

    class Meta:
        db_table = 'djangoAPI_UserTbl'

    def get_full_name(self):
        """
        Returns full name of user as defined in auth_user
        """
        return self.auth_user.first_name + ' ' + self.auth_user.last_name
# Project Tables


class SuperDesignProjectTbl(models.Model):
    '''Super set of design projects'''
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'djangoAPI_SuperDesignProjectTbl'


class DesignProjectTbl(models.Model):
    '''Table of Design Projects
    If a design project requires construction
    it will be linked to this table'''
    name = models.CharField(max_length=200)
    super_design_project = models.ForeignKey(
        SuperDesignProjectTbl, models.PROTECT, blank=True, null=True)
    phase_number = models.IntegerField(blank=True, null=True)
    op_bus_unit = models.ForeignKey(BusinessUnit, models.PROTECT)
    contract_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    planned_date_range = fields.DateRangeField(blank=True, null=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    # limited to 999B
    scope_description = models.TextField(blank=True, null=True)
    designer_organization_name = models.CharField(max_length=50)

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
        db_table = 'djangoAPI_DesignStageTbl'


class ConstructionPhaseTbl(models.Model):
    '''list all construction stages'''
    name = models.CharField(max_length=200)
    design_project = models.ForeignKey(DesignProjectTbl, models.SET_NULL, blank=True, null=True)
    phase_number = models.BigIntegerField(blank=True, null=True)
    op_bus_unit = models.ForeignKey(BusinessUnit, models.PROTECT)
    contract_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    planned_date_range = fields.DateRangeField(blank=True, null=True)
    scope_description = models.TextField()
    constructor_organization_name = models.CharField(max_length=50)

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


class MasterRoleNumbersTbl(models.Model):
    """
    Master List of all role numbers avaliable and in use
    """
    role_number = models.CharField(max_length=25, unique=True)
    project_tbl = models.ForeignKey(DesignProjectTbl, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'djangoAPI_MasterRoleNumbersTbl'

    @staticmethod
    def check_available(role_number, project_id):
        """
        Checks to see if a role number has been created.

        If it has been created check which project reserved it.

        If it is reserved check if it is used.
        """
        try:
            number = MasterRoleNumbersTbl.objects.get(role_number=role_number)
        except ObjectDoesNotExist:
            number = MasterRoleNumbersTbl.objects.create(
                role_number=role_number,
                project_tbl_id=project_id
            )
        else:
            if number.project_tbl_id != project_id:
                return Result(error_code=12, message='Role Number already reserved by another project')
            if list(ProjectAssetRoleRecordTbl.objects.filter(updatable_role_number_id=number.pk)):
                return Result(error_code=13, message='Role Number is already in use')
        finally:
            return Result(success=True, obj=number)


class ClonedAssetAndRoleInRegistryTbl(models.Model):
    '''From Avantis'''
    mtoi = models.AutoField(verbose_name="Avantis ID", primary_key=True)
    role_number = models.CharField(
        verbose_name="Entity Number", max_length=25, db_index=True, unique=True)
    role_name = models.CharField(verbose_name="Entity Name", max_length=200)
    parent_role_number = models.CharField(
        verbose_name="Parent Number", max_length=25, null=True, blank=True)
    # TODO bad practice to allow nulls for strings (default is empty string)
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
    # role_spatial_site_id = models.ForeignKey(ImportedSpatialSiteTbl, on_delete=models.PROTECT)
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
    linked_role_number = models.ForeignKey(MasterRoleNumbersTbl, models.PROTECT)

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
    db_table = models.ForeignKey(DBTbls, models.PROTECT)
    role = models.ForeignKey(to=AllHumanRoleTypeTbl, on_delete=models.PROTECT)
    permission_to_view = models.BooleanField()
    permission_to_update = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_AccessProfileDefinitionTbl'
        constraints = [
            models.UniqueConstraint(fields=['db_table', 'role'],
                                    name='one_permission_for_each_table_and_role_pair')
        ]


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
    updatable_role_number = models.ForeignKey(MasterRoleNumbersTbl, models.PROTECT)
    role_name = models.CharField(max_length=400)
    role_spatial_site_id = models.ForeignKey(ImportedSpatialSiteTbl, models.PROTECT)
    role_criticality = models.ForeignKey(RoleCriticality, models.PROTECT)
    role_priority = models.ForeignKey(RolePriority, models.PROTECT)
    project_tbl = models.ForeignKey(DesignProjectTbl, on_delete=models.PROTECT, null=True)
    approved = models.BooleanField(default=False)
    # to implement ltree, since the type isn't correctly this table will be unmanaged
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

    def remove_entity(self, project_id, entity_exists):
        """
        marks existing roles as does not exist
        deletes user added roles
        """
        if self.project_tbl_id != project_id:
            return Result(error_code=1, message='Role Reserved by Another Project')
        if not self.approved:
            return Result(error_code=2, message='Role Reservation not Approved')
        try:
            if self.missing_from_registry and not entity_exists:
                self.delete()
            else:
                self.entity_exists = entity_exists
                self.save()
        except Exception as e:
            return Result(success=False, error_code=3, message='Failed to Change Role Information', exception=e)
        return Result(success=True, obj_id=self.pk)


class NewProjectAssetRoleTbl(ProjectAssetRoleRecordTbl):
    new_role = models.BooleanField()

    class Meta:
        db_table = 'djangoAPI_NewProjectAssetRoleTbl'

    def remove_entity(self, project_id, entity_exists):
        """
        deletes new roles
        """
        if self.project_tbl_id != project_id:
            return Result(error_code=19, message='Role Reserved by Another Project')
        if not self.approved:
            return Result(error_code=20, message='Role Reservation not Approved')
        try:
            self.delete()
        except Exception as e:
            return Result(success=False, error_code=21, message='Failed to Delete Role', exception=e)
        return Result(success=True, obj_id=self.pk)


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

    def remove_entity(self, project_id, entity_exists):
        """
        Marks existing asset as non-existant
        removes user created asset 
        """
        if self.project_tbl_id != project_id:
            return Result(success=False, error_code=4, message='Asset Reserved by Another Project')
        try:
            if self.missing_from_registry and not entity_exists:
                self.delete()
            else:
                self.entity_exists = entity_exists
                self.save()
        except Exception as e:
            return Result(success=False, error_code=5, message='Failed to Change Asset Information', exception=e)
        return Result(success=True, obj_id=self.pk)


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

    def remove_entity(self, project_id, exists):
        """
        Removes self
        """
        if self.project_tbl_id != project_id:
            return Result(success=False, error_code=14, message='Asset Reserved by Another Project')
        try:
            self.delete()
        except Exception as e:
            return Result(success=False, error_code=15, message='Failed to Delete Asset', exception=e)
        return Result(success=True, obj_id=self.pk)


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
    approved = models.BooleanField(null=True)

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

    def remove_entity(self, project_id, exists):
        """
        marks existing roles and assets are non-existing
        removes user created roles and assets
        """
        role_id = self.pk
        try:
            asset = PreDesignReconciledAssetRecordTbl.objects.get(
                initial_project_asset_role_id_id=role_id)
        except ObjectDoesNotExist as e:
            pass
        else:
            result = asset.remove_entity(project_id, exists)
            if not result.success:
                return result
        try:
            role = PreDesignReconciledRoleRecordTbl.objects.get(pk=role_id)
        except ObjectDoesNotExist as e:
            return Result(success=False, error_code=6, message='Role Cannot be found')
        if not exists:  # removing
            child_roles = list(ProjectAssetRoleRecordTbl.objects.filter(parent_id_id=role_id))
            if child_roles:
                try:
                    for child in child_roles:
                        child.parent_id_id = 2
                        child.save()
                except Exception as e:
                    return Result(success=False, error_code=7, message='Failed to Orphan Children of role', exception=e)
        return role.remove_entity(project_id, exists)


class UnassignedAssetsView(models.Model):
    '''Read Only model using data from unassigned_assets'''
    # TODO this probably does not need to be a view, a filter probably works
    id = models.IntegerField(primary_key=True)
    asset_serial_number = models.TextField(null=True)
    asset_missing_from_registry = models.BooleanField(null=True)
    project_id = models.IntegerField(null=True)

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
            asset = ProjectAssetRecordTbl.objects.get(
                predesignreconciledassetrecordtbl__cloned_role_registry_tbl=key)
            role = ProjectAssetRoleRecordTbl.objects.get(
                predesignreconciledrolerecordtbl__cloned_role_registry_tbl=key)
        except Exception as e:
            return Result(success=False, message='Cannot find corresponding asset, are you sure this is an Avantis Asset?', exception=e, error_code=8)
        if asset.project_tbl != role.project_tbl:
            return Result(success=False, message='DB inconsistency error asset and role reserved by different projects. Please Contact Tony Huang', exception=e, error_code=9)
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
            return Result(success=False, message='Asset is reserved by another project group', error_code=10)
        try:
            asset.save()
            role.save()
        except Exception as e:
            return Result(success=False, message='Cannot change reservation', exception=e, error_code=11)
        else:
            return Result(success=True, obj_id=key)


class ChangeView(models.Model):
    """
    Read only model using data from change_view
    """
    id = models.IntegerField(primary_key=True)
    role_number = models.TextField(null=True)
    role_name = models.TextField(null=True)
    approved = models.BooleanField(null=True)
    parent = models.IntegerField(null=True)
    project_id = models.IntegerField(null=True)
    new_role = models.BooleanField(null=True)
    full_path = models.TextField(null=True)
    parent_changed = models.BooleanField(null=True)
    asset_id = models.IntegerField(null=True)
    asset_serial_number = models.TextField(null=True)
    role_changed = models.BooleanField(null=True)
    installation_stage_id = models.TextField(null=True)
    uninstallation_stage_id = models.TextField(null=True)
    new_asset = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = "change_view"

    @staticmethod
    def fixed_ltree(pk):
        '''retrives list of objects with fixed ltree'''
        lst = list(ChangeView.objects.filter(pk=pk))
        for l in lst:
            i = l.full_path.index('.')
            l.full_path = l.full_path[i+1:]
        return lst

    def remove_entity(self, project_id, exists=False):
        """
        Calls removal functions depending on if they are prexisting or new
        can only remove
        """
        new_role = self.new_role
        new_asset = self.new_asset
        role_id = self.pk
        if new_asset:
            try:
                asset = NewAssetDeliveredByProjectTbl.objects.get(
                    final_project_asset_role_id_id=role_id)
            except ObjectDoesNotExist as e:
                pass
        else:
            try:
                asset = PreDesignReconciledAssetRecordTbl.objects.get(
                    initial_project_asset_role_id_id=role_id)
            except ObjectDoesNotExist as e:
                pass
        result = asset.remove_entity(project_id, exists)
        if not result.success:
            return result

        if new_role:
            try:
                role = NewProjectAssetRoleTbl.objects.get(pk=role_id)
            except ObjectDoesNotExist as e:
                return Result(success=False, error_code=16, message='Role Cannot be found')
        else:
            try:
                role = PreDesignReconciledRoleRecordTbl.objects.get(pk=role_id)
            except ObjectDoesNotExist as e:
                return Result(success=False, error_code=17, message='Role Cannot be found')
        if not exists:  # removing
            child_roles = list(ProjectAssetRoleRecordTbl.objects.filter(parent_id_id=role_id))
            if child_roles:
                try:
                    for child in child_roles:
                        child.parent_id_id = 2
                        child.save()
                except Exception as e:
                    return Result(success=False, error_code=18, message='Failed to Orphan Children of role', exception=e)
        return role.remove_entity(project_id, exists)
