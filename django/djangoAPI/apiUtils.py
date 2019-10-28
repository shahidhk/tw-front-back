from .models import *
from django.db import transaction
import json


def AuthenticationUtil(info):
    '''Authenticates the User'''
    # consider changing to a class to replace dictionary
    data = {
        'valid': True,
        'approve': False,
        'group': None,
    }
    if info.context.META['HTTP_X_USERNAME'] == 'amber.brasher':
        data['group'] = 2
    elif info.context.META['HTTP_X_USERNAME'] == 'tony.huang':
        data['approve'] = True
        data['group'] = 2
    elif info.context.META['HTTP_X_USERNAME'] == 'jon.ma':
        data['approve'] = True
        data['group'] = 3
    else:
        data['group'] = 4
    return data


def ExplorationUtil(result):
    if result:
        return {'result': 1,
                'errors': 'you wanted an error so here it is'
                }
    else:
        return {'result': 0,
                'errors': 'No Errors'
                }


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
        with transaction.atomic():
            asset = PreDesignReconciledAssetRecordTbl()
            asset.designer_planned_action_type_tbl_id = 'c'
            asset.entity_exists = False
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


def AssignAssetToRoleUtil(data, auth):
    '''
    Assigns an Asset to a Role, Assign to null role for unassigned assets
    Expects Dictionary with asset_id, role_id
    Raises exception if another role is in that assets location
    '''

    if data['role_id'] is None or data['role_id'] == 0:
        data['role_id'] = None
    else:
        asset = list(PreDesignReconciledAssetRecordTbl.objects.filter(
            initial_project_asset_role_id_id=data['role_id']))
        if len(asset) != 0:
            return {'result': 1,
                    'errors': 'E6: An Asset is currently assigned to the role: ' + str(asset[0].pk)
                    }
        role = ProjectAssetRoleRecordTbl.objects.get(pk=data['role_id'])
        print(vars(role))
        if role.project_tbl_id != auth['group']:
            return {'result': 1,
                    'errors': 'E7: Role reserved by another project'
                    }
        elif not role.predesignreconciledrolerecordtbl.entity_exists:
            return {'result': 1,
                    'errors': 'E32: You are assigning an asset to a role that is marked as Non Existant'
                    }

    asset = ProjectAssetRecordTbl.objects.get(pk=data['asset_id'])
    if asset.project_tbl_id != auth['group']:
        return {'result': 1,
                'errors': 'E8: Asset reserved by another project'
                }
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(pk=data['asset_id'])
        asset.initial_project_asset_role_id_id = data['role_id']
        asset.save()
        return {'result': 0,
                'errors': data['role_id'] if data['role_id'] else 1,
                }
    except Exception as e:
        return {'result': 1,
                'errors': 'E9: Operation Failed ' + str(e) + ' ' + str(type(e))
                }


def DoesNotExistUtil(data, auth):
    '''
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
        return {'result': 1,
                'errors': 'E14: Asset cannot be found please refresh your View: ' + str(asset)
                }
    else:
        if existing_asset.project_tbl_id != auth['group']:
            return {'result': 1,
                    'errors': 'E15: Asset or Role reserved by another project'
                    }
        serial = existing_asset.asset_serial_number
        try:
            if existing_asset.missing_from_registry:
                # if the asset was created just delete it
                existing_asset.delete()
            else:
                existing_asset.designer_planned_action_type_tbl_id = 'b'
                existing_asset.save()
                retired_asset = ExistingAssetDisposedByProjectTbl(
                    predesignreconciledassetrecordtbl_ptr=existing_asset,
                    uninstallation_stage_id=0,
                )
                retired_asset.save_base(raw=True)
                # raw base save is required since the parent object has already been created
        except Exception as e:
            return {'result': 1,
                    'errors': 'E16: Operation Failed ' + str(e) + ' ' + str(type(e))
                    }
        else:
            return {'result': 0,
                    'errors': serial,
                    }


def RoleParentUtil(data, auth):
    '''
    Assigns a role to a parent
    takes in id of role and id of its new parent
    '''
    if data['role_id'] == data['parent_id']:
        return {'result': 1,
                'errors': 'E17: Cannot set the parent to be the same as the child'
                }
    try:
        role = data['role_id']
        role = ProjectAssetRoleRecordTbl.objects.get(id=role)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'E18: Role cannot be found please refresh your View: ' + str(data['role_id'])
                }
    else:
        if not role.predesignreconciledrolerecordtbl.entity_exists:
            return {'result': 1,
                    'errors': 'E33: You are assigning an role to a parent that is marked as Non Existant'
                    }
    if role.project_tbl_id != auth['group']:
        return {'result': 1,
                'errors': 'E19: Asset or Role reserved by another project'
                }
    if data['parent_id'] == 0:
        data['parent_id'] = None
    else:
        try:
            parent = data['parent_id']
            parent = ProjectAssetRoleRecordTbl.objects.get(id=parent)
        except Exception as e:
            print(str(type(e)))
            print(str(e))
            return {'result': 1,
                    'errors': 'E20: Parent role cannot be found please refresh your View: ' + str(data['parent_id'])
                    }
    try:
        role.parent_id_id = data['parent_id']
        role.save()
    except Exception as e:
        return {'result': 1,
                'errors': 'E21: Operation Failed ' + str(e) + ' ' + str(type(e))
                }
    else:
        return {'result': 0,
                'errors': role.pk,
                }


def ReserveEntityUtil(data, auth):
    '''Reserves Role and Asset for a project'''
    # if auth['approve']:
    #     return {'result': 1,
    #             'errors': 'E22: You are logged in as an Approver. Approvers are not allowed to change reservations',
    #             }
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(
            initial_project_asset_role_id_id=data['id'])
        role = ProjectAssetRoleRecordTbl.objects.get(pk=data['id'])
    except Exception as e:
        return {'result': 1,
                'errors': 'E23: Cannot find corresponding asset, are you sure this is an Avantis Asset? ' + str(e) + ' ' + str(type(e)),
                }
    else:
        if asset.project_tbl != role.project_tbl:
            return {'result': 1,
                    'errors': 'E24: DB inconsistency error asset and role reserved by different projects. Please Contact Tony Huang',
                    }
        if asset.project_tbl is None:  # asset is free real estate
            if data['reserved']:
                asset.project_tbl_id = auth['group']
                role.project_tbl_id = auth['group']
            else:  # dont return error if already unreserved
                return {'result': 0,
                        'errors': role.pk,
                        }
        elif asset.project_tbl_id == auth['group']:  # asset is reserved by this group
            if not data['reserved']:  # when reserved=False they are trying to unreserve
                asset.project_tbl = None
                role.project_tbl = None
                role.approved = False
            else:  # dont return error if already reservved
                return {'result': 0,
                        'errors': role.pk,
                        }
        else:  # asset is reserved by another group
            return {'result': 1,
                    'errors': 'E25: Asset is reserved by another project group',
                    }
        try:
            asset.save()
            role.save()
        except Exception as e:
            return {'result': 1,
                    'errors': 'E26: Cannot change reservation' + str(e) + ' ' + str(type(e)),
                    }
        else:
            return {'result': 0,
                    'errors': role.pk,
                    }


def ApproveReservationUtil(data, auth):
    '''approves reservations'''
    # if not auth['approve']:
    #     return {'result': 1,
    #             'errors': 'E27: User is unauthorized for approving assets. Please Login as Tony Huang.',
    #             }
    try:
        role = ProjectAssetRoleRecordTbl.objects.get(pk=data['id'])
    except Exception as e:
        return {'result': 1,
                'errors': 'E28: Cannot find corresponding entity, are you sure this entity exists? ' + str(e) + ' ' + str(type(e)),
                }
    else:
        if role.project_tbl is None:
            return {'result': 1,
                    'errors': 'E29: There are no pending reservation requests for this entity',
                    }
        else:
            role.approved = data['approved']
            if not data['approved']:
                # disapproving a reservation removes its reservation
                role.project_tbl_id = None
                try:
                    asset = PreDesignReconciledAssetRecordTbl.objects.get(
                        initial_project_asset_role_id_id=data['id'])
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
                        'errors': role.pk,
                        }
