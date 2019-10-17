from .models import *
from django.db import transaction
import json


def ExplorationUtil(result):
    if result:
        return {'result': 1,
                'errors': 'you wanted an error so here it is'
                }
    else:
        return {'result': 0,
                'errors': 'No Errors'
                }


def MissingRoleUtil(role_data):
    '''
    Adds a Role record that was missing from Avantis
    Checks to make sure role_number does not already exist
    '''
    if role_data['parent_id'] == 0:
        role_data['parent_id'] = None
    else:
        try:
            parent = ProjectAssetRoleRecordTbl.objects.get(
                pk=role_data['parent_id'])
        except Exception as e:
            print(str(type(e)))
            print(str(e))
            return {'result': 1,
                    'errors': 'Parent Does Not Exist ' + str(role_data['parent_id'])
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
                role.designer_planned_action_type_tbl_id = 3
                role.save()
                # pass the role pk back to the client?
        except Exception as e:
            return {'result': 1,
                    'errors': str(type(e)) + ' Operation Failed ' + str(e)
                    }
        return {'result': 0,
                'errors': role.pk,
                }
    else:
        return {'result': 1,
                'errors': 'There is already a role with this role number ' + str(role.pk)
                }


def MissingAssetUtil(asset_data):
    '''
    Adds an Asset record that was missing from Avantis
    '''
    try:
        with transaction.atomic():
            asset = PreDesignReconciledAssetRecordTbl()
            asset.designer_planned_action_type_tbl_id = 3
            asset.entity_exists = False
            asset.initial_project_asset_role_id = None
            asset.missing_from_registry = True
            asset.asset_serial_number = asset_data['asset_serial_number']
            asset.save()
    except Exception as e:
        return {'result': 1,
                'errors': str(type(e)) + ' Operation Failed ' + str(e)
                }
    return {'result': 0,
            'errors': asset.pk
            }


def AssignAssetToRoleUtil(data):
    '''
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
                    'errors': 'An Asset is currently assigned to the role: ' + str(asset[0].pk)
                    }
    with transaction.atomic():
        try:
            asset = PreDesignReconciledAssetRecordTbl.objects.get(
                pk=data['asset_id'])
            asset.initial_project_asset_role_id_id = data['role_id']
            asset.save()
            return {'result': 0,
                    'errors': data['role_id'],
                    }
        except Exception as e:
            return {'result': 1,
                    'errors': str(type(e)) + ' Operation Failed ' + str(e)
                    }


def DoesNotExistUtil(data):
    '''
    only look for the assets in preDesignReconciledAssetRecordTbl, roles in preDesignReconciledRoleRecordTbl
    will only look at the initial position of assets, not sure what happens if assets gets moved then you try to remove
    currently does not check for reservation / permissions
    '''
    role_id = data['role_id']
    dne = data['entity_exists']
    try:
        asset = PreDesignReconciledAssetRecordTbl.objects.get(
            initial_project_asset_role_id_id=role_id)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'Preexisting asset attached to this role cannot be found: ' + str(role_id)
                }
    try:
        role = PreDesignReconciledRoleRecordTbl.objects.get(pk=role_id)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'This role cannot be found please refresh your View: ' + str(role_id)
                }
    child_roles = list(
        ProjectAssetRoleRecordTbl.objects.filter(parent_id_id=role_id))
    # check for existance one by one * parent roles can be empty
    # it is pythonic to check to booleanness of the list to see if it is empty
    exist_childs = []
    if child_roles:
        for child in child_roles:
            if child.predesignreconciledrolerecordtbl.entity_exists:
                exist_childs.append(child)
        if exist_childs:
            child_roles = [child.pk for child in child_roles]
            return {'result': 1,
                    'errors': 'There are still roles that have not been removed : ' + str(child_roles)
                    }
    try:
        with transaction.atomic():
            asset.entity_exists = dne
            asset.save()
            role.entity_exists = dne
            role.save()
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': str(type(e)) + ' Error ' + str(e),
                }
    else:
        return {'result': 0,
                'errors': role.pk,
                }


def Authorization(auth_token):
    # TODO
    return True


def RetireAssetUtil(asset):
    '''
    Takes in asset ID not role ID!!
    Retire the Asset specified and leaves an empty role
    Currently defaults to landfill, and stage(0)
    '''
    # TODO if the asset was created just actually delete it
    try:
        existing_asset = PreDesignReconciledAssetRecordTbl.objects.get(
            pk=asset['asset_id'])
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'Asset cannot be found please refresh your View: ' + str(asset)
                }
    else:
        existing_asset.designer_planned_action_type_tbl_id = 2
        existing_asset.save()
    try:
        retired_asset = ExistingAssetDisposedByProjectTbl(
            predesignreconciledassetrecordtbl_ptr=existing_asset,
            uninstallation_stage_id=0,
        )
        retired_asset.save_base(raw=True)
    except Exception as e:
        return {'result': 1,
                'errors': str(type(e)) + ' Operation Failed ' + str(e)
                }
    else:
        return {'result': 0,
                'errors': existing_asset.asset_serial_number,
                }


def RoleParentUtil(data):
    '''
    takes in id of role and id of its new parent
    '''
    if data['role_id'] == data['parent_id']:
        return {'result': 1,
                'errors': 'Cannot set the parent to be the same as the child'
                }
    try:
        role = data['role_id']
        role = ProjectAssetRoleRecordTbl.objects.get(id=role)
    except Exception as e:
        print(str(type(e)))
        print(str(e))
        return {'result': 1,
                'errors': 'Role cannot be found please refresh your View: ' + str(data['role_id'])
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
                    'errors': 'Parent role cannot be found please refresh your View: ' + str(data['parent_id'])
                    }

    try:
        role.parent_id_id = data['parent_id']
        role.save()
    except Exception as e:
        return {'result': 1,
                'errors': str(type(e)) + ' Operation Failed ' + str(e)
                }
    else:
        return {'result': 0,
                'errors': role.pk,
                }
