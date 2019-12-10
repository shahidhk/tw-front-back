from .models import *
from django.db import transaction
import json


def AuthenticationUtil(info):
    '''Authenticates the User'''
    # consider changing to a class to replace dictionary
    USER_PERMISSIONS = {
        'amber.brasher': {
            'valid': True,
            'group': [2, 3, ],
            'user_id': 3,
            'approve': False,
        },
        'tony.huang': {
            'valid': True,
            'group': [2, 3, ],
            'user_id': 2,
            'approve': True,
        },
        'jon.ma': {
            'valid': True,
            'group': [4, ],
            'user_id': 4,
            'approve': True,
        },
    }
    try:
        user = USER_PERMISSIONS[info.context.META['HTTP_X_USERNAME']]
    except KeyError:
        raise Exception('The user specified cannot be found: ' +
                        info.context.META['HTTP_X_USERNAME'])
    else:
        if int(info.context.META['HTTP_X_PROJECT']) in user['group']:
            user['group'] = int(info.context.META['HTTP_X_PROJECT'])
        else:
            # User Does Not belong to the project specified in the header
            # instead of raising an exception we set valid to false, this way non project required mutations can still run if needed
            # ex getting projects of a user
            user['valid'] = False
    return user


def add_missing_role_asset(role_data, change_type, auth):
    # TODO need general function for checking if role is in use
    # currently these add functions do not check if role is in use, which can result in double assignment to a role
    """
    Adds a Role / Asset record that was missing from Avantis
    add_type:
        1 - Add both new asset and role
        2 - add role with no asset (for associating with an existing asset)
        3 - add asset to a role (for associating to an existing role)
    """
    if change_type == 3:
        try:
            role = ProjectAssetRoleRecordTbl.objects.get(pk=role_data['id'])
        except ObjectDoesNotExist:
            return Result(success=False, error_code=200, message='Role Cannot be found')
    else:
        role_number_obj = MasterRoleNumbersTbl.check_available(role_data['role_number'], auth['group'])
        if role_number_obj.success:
            try:
                role = PreDesignReconciledRoleRecordTbl.objects.create(
                    updatable_role_number=role_number_obj.obj,
                    role_name=role_data['role_name'],
                    parent_id_id=role_data['parent_id'],
                    role_criticality_id=role_data['role_criticality'],
                    role_priority_id=role_data['role_priority'],
                    role_spatial_site_id_id=role_data['role_spatial_site_id'],
                    entity_exists=True,
                    missing_from_registry=True,
                    designer_planned_action_type_tbl_id='c',
                    parent_changed=False,
                    project_tbl_id=auth['group'],
                    approved=True,
                )
            except ObjectDoesNotExist as e:
                return Result(message='Parent Does Not Exist: ' + str(role_data['parent_id']), error_code=100)
            except Exception as e:
                return Result(message='Failed to Create Role', exception=e, error_code=201)
        else:
            return role_number_obj
    if change_type == 2: # if we only want a new role we are done now
        pass # we will use the return at the end since its the same
    else:
        asset = PreDesignReconciledAssetRecordTbl(
            project_tbl_id=auth['group'],
            asset_serial_number=role_data['asset_serial_number'],
            entity_exists=True,
            missing_from_registry=True,
            initial_project_asset_role_id=role,
            designer_planned_action_type_tbl_id='c',
        )
        try:
            asset.save()
        except Exception as e:
            return Result(success=False, error_code=202, message='Failed to Create Asset', exception=e)
    return Result(success=True, obj_id=role.pk, obj=role)


def MissingRoleUtil(role_data, auth):
    '''
    Adds a Role record that was missing from Avantis
    Checks to make sure role_number does not already exist
    '''
    if role_data['parent_id'] == 0:
        return {'result': 1,
                'errors': 'E1: Deprecated: Top level assets should have parent set to 1',
                }
    else:
        try:
            parent = ProjectAssetRoleRecordTbl.objects.get(
                pk=role_data['parent_id'])
        except Exception as e:
            print(str(type(e)))
            print(str(e))
            return {'result': 1,
                    'errors': 'E2: Parent Does Not Exist ' + str(role_data['parent_id'])
                    }
    try:
        role = ProjectAssetRoleRecordTbl.objects.get(
            updatable_role_number=role_data['role_number'])
    except ProjectAssetRoleRecordTbl.DoesNotExist:
        try:
            with transaction.atomic():
                role = PreDesignReconciledRoleRecordTbl()
                role.updatable_role_number = role_data['role_number']
                role.role_name = role_data['role_name']
                role.parent_id_id = role_data['parent_id']
                role.role_criticality_id = role_data['role_criticality']
                role.role_priority_id = role_data['role_priority']
                role.role_spatial_site_id_id = role_data['role_spatial_site_id']
                role.entity_exists = True
                role.missing_from_registry = True
                role.designer_planned_action_type_tbl_id = 'c'
                role.parent_changed = False
                role.project_tbl_id = auth['group']
                role.approved = True
                role.save()
                # pass the role pk back to the client?
        except Exception as e:
            return {'result': 1,
                    'errors': 'E3: Operation Failed ' + str(e) + ' ' + str(type(e))
                    }
        return {'result': 0,
                'errors': role.pk,
                }
    else:
        return {'result': 1,
                'errors': 'E4: There is already a role with this role number ' + str(role.pk)
                }


def MissingAssetUtil(asset_data, auth):
    '''
    Adds an Asset record that was missing from Avantis
    '''

    try:
        asset = PreDesignReconciledAssetRecordTbl()
        asset.designer_planned_action_type_tbl_id = 'c'
        asset.entity_exists = True
        asset.initial_project_asset_role_id = None
        asset.missing_from_registry = True
        asset.asset_serial_number = asset_data['asset_serial_number']
        asset.role_changed = False
        asset.project_tbl_id = auth['group']
        asset.save()
    except Exception as e:
        return {'result': 1,
                'errors': 'E5: Operation Failed ' + str(e) + ' ' + str(type(e))
                }
    return {'result': 0,
            'errors': asset.pk
            }


def assign_asset_to_role_reconciliation(data, auth):
    '''
    Assigns an Asset to a Role, Assign to null role for unassigned assets
    Expects Dictionary with asset_id, role_id
    Raises exception if another role is in that assets location
    '''
    role = None
    if data['role_id'] is None or data['role_id'] == 0:
        data['role_id'] = None
    else:
        asset = list(PreDesignReconciledAssetRecordTbl.objects.filter(
            initial_project_asset_role_id_id=data['role_id']))
        if len(asset) != 0:
            return Result(message='An Asset is currently assigned to the role: ' + str(asset[0].pk), error_code=400)
        role = ProjectAssetRoleRecordTbl.objects.get(pk=data['role_id'])
        if role.project_tbl_id != auth['group']:
            return Result(message='Role reserved by another project', error_code=401)
        elif not role.predesignreconciledrolerecordtbl.entity_exists:
            return Result(message='You are assigning an asset to a role that is marked as Non Existant', error_code=402)
        elif not role.approved:
            return Result(message='The reservation for this entity has not been approved', error_code=403)
    asset = ProjectAssetRecordTbl.objects.get(pk=data['asset_id'])
    if asset.project_tbl_id != auth['group']:
        return Result(message='Asset reserved by another project', error_code=404)
    asset = PreDesignReconciledAssetRecordTbl.objects.get(pk=data['asset_id'])
    if asset.initial_project_asset_role_id:  # if asset gets moved to unassigned asset it will not have a role
        # TODO approval for both asset and roles
        if not asset.initial_project_asset_role_id.approved:
            return Result(message='The reservation for this entity has not been approved', error_code=405)
    if asset.designer_planned_action_type_tbl_id == 'b':
        asset.designer_planned_action_type_tbl_id = 'c'
        asset_dispose = ExistingAssetDisposedByProjectTbl.objects.get(pk=asset.pk)
        asset_dispose.delete(keep_parents=True)
    try:
        asset.initial_project_asset_role_id_id = data['role_id']
        asset.save()
        return Result(success=True, obj=role, obj_id=data['role_id'])
    except Exception as e:
        return Result(message='Operation Failed', exception=e, error_code=406)


def remove_reconciliation_asset(data, auth):
    """
    Marks existing asset as non-existant
    deletes user created asset
    """
    asset_id = data['asset_id']
    project_id = auth['group']
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(pk=asset_id)
    except ObjectDoesNotExist as e:
        return Result(error_code=900, message='Asset cannot be found')
    else:
        return asset.remove_reconciliation(project_id)


def remove_reconciliation(data, auth):
    """
    Marks Existing Assets & Role as Non-Existant
    Deletes User Created Role & Asset
    """
    role_id = data['role_id']
    project_id = auth['group']
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(
            initial_project_asset_role_id_id=role_id)
    except ObjectDoesNotExist as e:
        pass
    else:
        result = asset.remove_reconciliation(project_id)
        if not result.success:
            return result
    try:
        role = PreDesignReconciledRoleRecordTbl.objects.get(pk=role_id)
    except ObjectDoesNotExist as e:
        return Result(error_code=500, message='Role Cannot be found')
    child_roles = list(ProjectAssetRoleRecordTbl.objects.filter(parent_id_id=role_id))
    if child_roles:
        try:
            for child in child_roles:
                # if child.predesignreconciledassetrecordtbl.entity_exists:
                # TODO currently deleted children are moved to orphan state (but still shows in deleted view) when their parent gets deleted
                child.parent_id_id = 2
                child.save()
        except Exception as e:
            return Result(error_code=501, message='Failed to Orphan Children of role', exception=e)
    result = role.remove_reconciliation(project_id)
    if result.success:
        return Result(success=True, obj_id=role.pk)
    else:
        return result


def remove_change(role_id, auth):
    """
    Unassign all children and move entity to removed view
    """
    try:
        entity = ChangeView.objects.get(pk=role_id)
    except Exception as e:
        return Result(message='This entity does not exist', exception=e, error_code=700)
    return entity.remove_entity(auth['group'])


def unremove_asset(asset_id, auth):
    try:
        asset = ProjectAssetRecordTbl.objects.get(pk=asset_id)
    except ObjectDoesNotExist:
        return {'result': 1,
                'errors': 'E:H:' + Result(message='This Asset does not exist', error_code=-11).readable_message(),
                }
    else:
        asset.unremove(auth)


def unremove_role(role_id, auth):
    """
    Unremoves the role and asset if attached
    """
    try:
        role = ProjectAssetRoleRecordTbl.objects.get(pk=role_id)
    except ObjectDoesNotExist:
        return {'result': 1,
                'errors': 'E:G:' + Result(message='This Role does not exist', error_code=-10).readable_message(),
                }
    else:
        role.unremove(auth)
    asset = get_asset_by_role_id(role_id)
    if asset: # if an asset gets returned
        unremove_asset(asset.pk, auth)


def get_asset_by_role_id(role_id):
    try:
        asset = NewAssetDeliveredByProjectTbl.objects.get(final_project_asset_role_id_id=role_id)
    except ObjectDoesNotExist:
        pass
    else:
        return asset
    try:
        asset = ExistingAssetMovedByProjectTbl.objects.get(final_project_asset_role_id_id=role_id)
    except ObjectDoesNotExist:
        pass
    else:
        return asset
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(initial_project_asset_role_id_id=role_id)
    except ObjectDoesNotExist:
        pass
    else:
        return asset
    return None


def DoesNotExistUtil(data, auth):
    '''
    Deprecated
    Marks Asset and Role as Does Not Exist
    only look for the assets in preDesignReconciledAssetRecordTbl, roles in preDesignReconciledRoleRecordTbl
    will only look at the initial position of assets, not sure what happens if assets gets moved then you try to remove
    '''
    role_id = data['role_id']
    entity_exists = data['entity_exists']
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(
            initial_project_asset_role_id_id=role_id)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'E10: Preexisting asset attached to this role cannot be found: ' + str(role_id)
                }
    try:
        role = PreDesignReconciledRoleRecordTbl.objects.get(pk=role_id)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'E11: This role cannot be found please refresh your View: ' + str(role_id)
                }
    if asset.project_tbl_id != auth['group'] or role.project_tbl_id != auth['group']:
        return {'result': 1,
                'errors': 'E12: Asset or Role reserved by another project',
                }
    elif not role.approved:
        return {'result': 1,
                'errors': 'E35: The reservation for this entity has not been approved'
                }
    child_roles = list(ProjectAssetRoleRecordTbl.objects.filter(parent_id_id=role_id))

    # children are orphaned when parents get 'removed'

    try:
        with transaction.atomic():
            if child_roles:
                for child in child_roles:
                    child.parent_id_id = 2
                    child.save()
            if not entity_exists:
                # some logic for deleting roles / assets
                if asset.missing_from_registry and role.missing_from_registry:
                    asset.delete()
                    role.delete()
                elif asset.missing_from_registry:
                    asset.delete()
                    role.entity_exists = entity_exists
                    role.save()
                elif role.missing_from_registry:
                    role.delete()
                    asset.entity_exists = entity_exists
                    asset.save()
                else:
                    asset.entity_exists = entity_exists
                    asset.save()
                    role.entity_exists = entity_exists
                    role.save()
            else:
                asset.entity_exists = entity_exists
                asset.save()
                role.entity_exists = entity_exists
                role.save()
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'E13: Operation Failed ' + str(e) + ' ' + str(type(e))
                }
    else:
        return {'result': 0,
                'errors': role.pk,
                }


def RetireAssetUtil(asset, auth):
    '''
    Retire the Asset specified and leaves an empty role
    Currently defaults to landfill, and stage(0)
    Takes in asset ID not role ID!!
    '''
    try:
        existing_asset = PreDesignReconciledAssetRecordTbl.objects.get(pk=asset['asset_id'])
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return Result(message='Asset cannot be found please refresh your View: ' + str(asset), error_code=1000)
    else:
        if existing_asset.project_tbl_id != auth['group']:
            return Result(message='Asset or Role reserved by another project', error_code=1001)
        serial = existing_asset.asset_serial_number
        try:
            if existing_asset.missing_from_registry:
                # if the asset was created just delete it
                existing_asset.delete()
            else:
                existing_asset.designer_planned_action_type_tbl_id = 'b'
                existing_asset.entity_exists = False
                existing_asset.save()
                retired_asset = ExistingAssetDisposedByProjectTbl(
                    predesignreconciledassetrecordtbl_ptr=existing_asset,
                    uninstallation_stage_id=1,  # TODO
                )
                retired_asset.save_base(raw=True)
                # raw base save is required since the parent object has already been created
        except Exception as e:
            return Result(message='Operation Failed', error_code=1002, exception=e)
        else:
            return Result(success=True, obj_id=existing_asset.pk)


def remove_asset(data, auth):
    """
    Takes in the assets id and removes the asset
    calls RetireAssetUtil for existing assets
    """
    try:
        asset = ProjectAssetRecordTbl.objects.get(pk=data['asset_id'])
    except Exception as e:
        return Result(message='Asset does not exist', exception=e, error_code=800)
    try:
        asset = NewAssetDeliveredByProjectTbl.objects.get(pk=data['asset_id'])
    except Exception as e:
        return RetireAssetUtil(asset, auth)
    else:
        try:
            asset.delete()
        except Exception as e:
            return Result(message='Cannot delete user created asset', exception=e, error_code=801)
        else:
            return Result(success=True, obj_id=None, obj=None)

def change_role_parent(data, auth):
    '''
    Assigns a role to a parent
    takes in id of role and id of its new parent
    '''
    if data['role_id'] == data['parent_id']:
        return Result(message='Cannot set the parent to be the same as the child', error_code=300)
    try:
        role = ProjectAssetRoleRecordTbl.objects.get(id=data['role_id'])
    except Exception as e:
        return Result(message='Role cannot be found please refresh your View', exception=e, error_code=301)
    if role.project_tbl_id != auth['group']:
        return Result(message='Entity unreserved or reserved by another project', error_code=302)
    if not role.approved:
        return Result(message='The reservation for this entity has not been approved', error_code=303)
    if data['parent_id'] == 0:
        data['parent_id'] = None
    else:
        try:
            parent = ProjectAssetRoleRecordTbl.objects.get(id=data['parent_id'])
        except Exception as e:
            return Result(message='Parent role cannot be found please refresh your View: ' + str(data['parent_id']), error_code=304)
        if str(role.pk) in parent.ltree_path.split('.'):
            return Result(message='E40: This action will create a circular reference: ' + role.role_name + ' is in hierarchy of ' + parent.role_name, error_code=305)
        try:  # if the role is prexisting make sure its not marked as non existant
            if not parent.predesignreconciledrolerecordtbl.entity_exists:
                return Result(message='You are assigning an role to a parent that is marked as Non Existant', error_code=306)
        except Exception:
            pass
    try:
        unremove_role(role.pk, auth)
        role.parent_id_id = data['parent_id']
        role.save()
    except Exception as e:
        return Result(message='Operation Failed', error_code=307, exception=e)
    else:
        return Result(success=True, obj_id=role.pk, obj=role)


def ReserveEntityUtil(data, auth):
    '''Reserves Role and Asset for a project'''
    # Note this function uses a class method, not sure if this is better
    try:
        reserve = ReservationView.objects.get(pk=data['id'])
    except Exception as e:
        return {'result': 1,
                'errors': 'E:A:' + Result(message='This entity does not exist', exception=e, error_code=-2).readable_message(),
                }
    result = reserve.change_reservation(auth['group'], data['reserved'])
    if result.success:
        return {'result': 0,
                'errors': result.obj_id,
                }
    else:
        return {'result': 1,
                'errors': 'E:A:' + result.readable_message(),
                }


def ApproveReservationUtil(data, auth):
    '''approves reservations'''
    if not auth['approve']:
        return {'result': 1,
                'errors': 'E27: User is unauthorized for approving assets. Please Login as an Approver.',
                }
    try:
        role = ProjectAssetRoleRecordTbl.objects.get(
            predesignreconciledrolerecordtbl__cloned_role_registry_tbl=data['id'])
    except Exception as e:
        return {'result': 1,
                'errors': 'E28: Cannot find corresponding entity, are you sure this entity exists? ' + str(e) + ' ' + str(type(e)),
                }
    else:
        if role.project_tbl is None:
            return {'result': 1,
                    'errors': 'E29: There are no pending reservation requests for this entity',
                    }
        if role.project_tbl_id != auth['group']:
            return {'result': 1,
                    'errors': 'E39: You are not an approver for this Project',
                    }
        else:
            role.approved = data['approved']
            if not data['approved']:
                # disapproving a reservation removes its reservation
                role.project_tbl_id = None
                try:
                    asset = PreDesignReconciledAssetRecordTbl.objects.get(
                        cloned_role_registry_tbl=data['id'])
                    asset.project_tbl_id = None
                    asset.save()
                except Exception as e:
                    return {'result': 1,
                            'errors': 'E31: Cannot change reservation for attached asset' + str(e) + ' ' + str(type(e)),
                            }
            try:
                role.save()
            except Exception as e:
                return {'result': 1,
                        'errors': 'E30: Cannot change reservation' + str(e) + ' ' + str(type(e)),
                        }
            else:
                return {'result': 0,
                        'errors': data['id'],
                        }


def add_new_role_asset(data, change_type, auth):
    # TODO need general function for checking if role is in use
    # currently these add functions do not check if role is in use, which can result in double assignment to a role
    """
    Creates a new role / asset
    type 1: new role + asset
    type 2: new role
    type 3: new asset
    """
    if change_type != 3:
        role_number_obj = MasterRoleNumbersTbl.check_available(data['role_number'], auth['group'])
        if not role_number_obj.success:
            return role_number_obj
    return ChangeView.add_entity(data, change_type, auth)
        

def assign_asset_to_role_change(data, auth):
    # TODO consider merging with assign_asset_to_role_reconciliation(data, auth):
    if data['role_id'] is None or data['role_id'] == 0:
        data['role_id'] = None
        role = None
    else:
        asset = list(PreDesignReconciledAssetRecordTbl.objects.filter(
            initial_project_asset_role_id_id=data['role_id']))
        if len(asset) == 0:
            asset = list(NewAssetDeliveredByProjectTbl.objects.filter(
                final_project_asset_role_id_id=data['role_id']))
        if len(asset) == 0:
            asset = list(ExistingAssetMovedByProjectTbl.objects.filter(
                final_project_asset_role_id_id=data['role_id']))
        if len(asset) != 0:
            return Result(message='Another Asset is currently assigned to this role: '  + str(asset[0].asset_serial_number), error_code=600)
        role = ProjectAssetRoleRecordTbl.objects.get(pk=data['role_id'])
        if role.project_tbl_id != auth['group']:
            return Result(message='Role reserved by another project', error_code=601)
        elif not role.approved:
            return Result(message='The reservation for this entity has not been approved', error_code=602)
        try:
            if not role.predesignreconciledrolerecordtbl.entity_exists:
                return Result(message='You are assigning an asset to a role that is marked as Non Existant', error_code=603)
        except Exception:
            pass

    asset = ProjectAssetRecordTbl.objects.get(pk=data['asset_id'])
    if asset.project_tbl_id != auth['group']:
        return Result(message='Asset reserved by another project', error_code=604)
    try:
        if asset.predesignreconciledassetrecordtbl:
            moved = ExistingAssetMovedByProjectTbl(
                predesignreconciledassetrecordtbl_ptr=asset.predesignreconciledassetrecordtbl,
                final_project_asset_role_id_id=role.pk,
                installation_stage_id=1,
                uninstallation_stage_id=1,
            )
            moved.save_base(raw=True)
            # remove new entry if reverted to original parent
    except Exception:
        pass
    try:
        if asset.newassetdeliveredbyprojecttbl:
            asset.newassetdeliveredbyprojecttbl.final_project_asset_role_id_id = role.pk
            asset.save()
            asset.newassetdeliveredbyprojecttbl.save() #TODO not sure which one is necessary
    except Exception:
        pass
    return Result(success=True, obj=role, obj_id=data['role_id'])
        