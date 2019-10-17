import csv
import json
import random
from datetime import date, timedelta

from django.db import transaction, connection
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoAPI.models import *
from djangoAPI.utils import num_to_alpha


def init_db(request):
    '''
    Initilize the DB with extensions, views and ltree specific triggers
    '''
    with connection.cursor() as cursor:
        try:
            cursor.execute('CREATE EXTENSION ltree;')
        except Exception as e:
            print(type(str(e)))
            print(str(e))
        try:
            cursor.execute('''ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl" DROP COLUMN ltree_path;
        ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl"
            ADD COLUMN ltree_path ltree;
        CREATE INDEX parent_id_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" USING GIST (ltree_path);
        CREATE INDEX parent_path_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" (parent_id_id);''')
        except Exception as e:
            print(type(str(e)))
            print(str(e))
        try:
            cursor.execute(
                '''
        CREATE OR REPLACE FUNCTION update_parent_path() RETURNS TRIGGER AS $$
            DECLARE
                path ltree;
            BEGIN
                IF NEW.parent_id_id IS NULL THEN
                    NEW.ltree_path = ((new.id::text)::ltree);
                ELSEIF TG_OP = 'INSERT' OR OLD.parent_id_id IS NULL OR OLD.parent_id_id != NEW.parent_id_id THEN
                    SELECT ltree_path FROM public."djangoAPI_ProjectAssetRoleRecordTbl" WHERE id = NEW.parent_id_id INTO path;
                    IF path IS NULL THEN
                        RAISE EXCEPTION 'Invalid parent_id %. Entities must be added parents first', NEW.parent_id_id;
                    END IF;
                    path = path || new.id::text;
                    NEW.ltree_path = path;
                    UPDATE public."djangoAPI_ProjectAssetRoleRecordTbl"
                        SET ltree_path = path || subpath(ltree_path,nlevel(OLD.ltree_path)) WHERE ltree_path <@ OLD.ltree_path and ltree_path != old.ltree_path;
                END IF;
                RETURN NEW;
            END;
        $$ LANGUAGE plpgsql;
        ''')
        except Exception as e:
            print(type(str(e)))
            print(str(e))
        try:
            cursor.execute(
                '''
        CREATE TRIGGER parent_path_tgr
            BEFORE INSERT OR UPDATE ON public."djangoAPI_ProjectAssetRoleRecordTbl"
            FOR EACH ROW EXECUTE PROCEDURE update_parent_path();
        ''')
        except Exception as e:
            print(type(str(e)))
            print(str(e))
        cursor.execute(
            '''
        create or replace view reconciliation_view as
        select
        r.id, r.updatable_role_number as role_number,
        r.role_name as role_name,
        r.parent_id_id as parent,
        r.project_tbl_id as project_id,
        r.entity_exists as role_exists,
        r.missing_from_registry as role_missing_from_registry,
        r.ltree_path as full_path,
        a.id as asset_id,
        a.asset_serial_number as asset_serial_number,
        a.entity_exists as asset_exists,
        a.missing_from_registry as asset_missing_from_registry
        from (
        public."djangoAPI_ProjectAssetRoleRecordTbl" as br
        right join public."djangoAPI_PreDesignReconciledRoleRecordTbl" as pr
        on (br.id=pr.projectassetrolerecordtbl_ptr_id)) as r
        left join (
        public."djangoAPI_PreDesignReconciledAssetRecordTbl" as pa
        left join public."djangoAPI_ProjectAssetRecordTbl" as ba
        on (pa.projectassetrecordtbl_ptr_id=ba.id)) as a
        on (r.id=a.initial_project_asset_role_id_id);
        ''')
        cursor.execute(
            '''
        create or replace view unassigned_assets as
        select ba.id as id, ba.asset_serial_number as asset_serial_number
        from public."djangoAPI_PreDesignReconciledAssetRecordTbl" as pa
        left join public."djangoAPI_ProjectAssetRecordTbl" as ba
        on pa.projectassetrecordtbl_ptr_id=ba.id
        where pa.initial_project_asset_role_id_id is null and pa.designer_planned_action_type_tbl_id<>'b';
        ''')
        cursor.execute('''
        create or replace
        view reservation_view as
        select
            id,
            updatable_role_number as role_number,
            role_name,
            parent_id_id as parent,
            project_tbl_id as project_id,
            ltree_path as full_path,
            approved,
            (not project_tbl_id is null) as reserved
        from
            public."djangoAPI_ProjectAssetRoleRecordTbl" ;
        ''')
        return HttpResponse("Finished DB init")


def db_fill(request):
    '''
    Fill the DB with test data
    Will eventually switch to initialization with constants for list tables
    '''
    InitEnums()
    InitValueList()
    for i in range(3):
        DesignProjectTbl.objects.create(
            pk=i+1,
            planned_date_range=(date.today(), date.today() + timedelta(days=40)),
            op_bus_unit_id=['a', 'b', 'c'][i],
        )
    lst = [['Tony', 'Huang'], ['Peter', 'Lewis'], ['Stephen', 'Almeida']]
    for i, value in enumerate(lst):
        UserTbl.objects.create(
            id=i+1,
            first_name=value[0],
            last_name=value[1],
            username=value[0]+'.'+value[1],
            organization_name='TW',
            email=value[0]+'.'+value[1]+'@admin.ca',
            user_type_id=1,
        )
    for i in range(3):
        for j in range(3):
            DesignProjectHumanRoleTbl.objects.create(
                user_id_id=j+1,
                design_project_id=i+1,
                human_role_type_id=num_to_alpha(j+1),
            )
    today = date.today()
    for i in range(2):
        today = today + timedelta(days=5)
        for j in range(3):
            DesignStageTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=5), today),
                design_stage_type_id=[
                    'a', 'b', 'c', 'd', 'e'][j],
                design_project_id=j+1,
            )
    today = date.today() + timedelta(days=10)
    for i in range(2):
        today = today + timedelta(days=15)
        for j in range(3):
            ConstructionPhaseTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=15), today),
                phase_number=i,
                design_project_id=j + 1,
                scope_description='a project construction phase',
                op_bus_unit_id=['a', 'b', 'c'][i],
            )
    for i in range(3):
        for j in range(3):
            ConstructionPhaseHumanRoleTbl.objects.create(
                user_id_id=j+1,
                construction_phase_id=i+1,
                human_role_type_id=num_to_alpha(j+1),
            )
    today = date.today() + timedelta(days=10)
    for i in range(2):
        today = today + timedelta(days=5)
        for j in range(3):
            ConstructionStageTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=5), today),
                construction_phase_id=i+1,
                construction_stage_type_id=[
                    'a', 'b', 'c', 'd', 'e'][j],
            )
    asset_line = {}
    with open('avantis.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count = line_count + 1
            asset_line[row[0]] = [line_count, row]
    with transaction.atomic():
        # TODO When creating location tags, remove duplicates, get dictionary of locations
        for asset_row in asset_line.items():
            spatial_site = ImportedSpatialSiteTbl()
            spatial_site.pk = asset_row[1][0]
            spatial_site.name = asset_row[1][1][7]
            try:
                spatial_site.parentSiteId_id = asset_line[asset_row[1][1][3]][0]
            except Exception:
                spatial_site.parentSiteId_id = None
            spatial_site.save()
    for asset_row in asset_line.items():
        avantis_asset = ClonedAssetAndRoleInRegistryTbl()
        avantis_asset.mtoi = asset_row[1][0]
        avantis_asset.role_number = asset_row[0]
        avantis_asset.role_name = asset_row[1][1][1]
        avantis_asset.parent_role_number = asset_row[1][1][3]
        avantis_asset.role_location = asset_row[1][1][7]
        avantis_asset.role_criticality = asset_row[1][1][6]
        avantis_asset.role_priority = 5  # did not exist in my avantis import
        avantis_asset.role_equipment_type = 'meh'
        avantis_asset.role_classification = 'does this even matter right now?'
        avantis_asset.asset_serial_number = 'dont have this value either'
        avantis_asset.suspension_id_id = 1
        avantis_asset.already_reserved_id = 1
        avantis_asset.intent_to_reserve_id = 1
        avantis_asset.role_spatial_site_id_id = asset_row[1][0]
        avantis_asset.save()
    return HttpResponse("Finished DB Fill")


def update_asset_role(request):
    cloned_assets = ClonedAssetAndRoleInRegistryTbl.objects.all()
    parent_mtoi = {}  # dictionary for quickly finding entry by role number
    for entry in cloned_assets:  # populate dict, keys = role number
        if entry.role_number in parent_mtoi.keys():
            pass
        else:
            parent_mtoi[entry.role_number] = entry

    base_role_dict = {}  # dictionary for tracking roles and its pk
    with transaction.atomic():
        for entry in cloned_assets:
            existing_role = PreDesignReconciledRoleRecordTbl()
            existing_role.updatable_role_number = entry.role_number
            existing_role.role_name = entry.role_name
            existing_role.parent_id_id = None  # fill this in on the second go
            existing_role.role_criticality_id = num_to_alpha(
                entry.role_criticality)
            existing_role.role_priority_id = num_to_alpha(entry.role_priority)
            existing_role.role_spatial_site_id = entry.role_spatial_site_id
            existing_role.cloned_role_registry_tbl_id = parent_mtoi[entry.role_number].mtoi
            existing_role.entity_exists = True
            existing_role.missing_from_registry = False
            existing_role.designer_planned_action_type_tbl_id = num_to_alpha(
                3)  # do nothing
            existing_role.save()
            base_role_dict[existing_role.updatable_role_number] = existing_role.pk
    base_roles = ProjectAssetRoleRecordTbl.objects.all()
    # with transaction.atomic():
    for role in base_roles:
        try:
            role.parent_id_id = base_role_dict[parent_mtoi[role.updatable_role_number].parent_role_number]
            role.save()
        except Exception as e:
            print('cant save parent for ' +
                  role.updatable_role_number + str(type(e)) + str(e))
        else:
            print('saved parent for ' + role.updatable_role_number)
    # populate predesign asset records
    with transaction.atomic():
        for entry in cloned_assets:
            existing_asset = PreDesignReconciledAssetRecordTbl()
            existing_asset.asset_serial_number = 'disguised asset serial number'
            existing_asset.cloned_role_registry_tbl_id = parent_mtoi[entry.role_number].mtoi
            existing_asset.initial_project_asset_role_id_id = base_role_dict[entry.role_number]
            existing_asset.entity_exists = True
            existing_asset.missing_from_registry = False
            existing_asset.designer_planned_action_type_tbl_id = num_to_alpha(
                3)  # do nothing
            existing_asset.save()
    return HttpResponse('Finished Updating Asset & Role')


def test(request):
    base_assets = PreDesignReconciledAssetRecordTbl.objects.all()
    with transaction.atomic():
        for asset in base_assets:
            asset.asset_serial_number = 'role # ' + \
                str(asset.initial_project_asset_role_id_id) + \
                'asset serial number'
            asset.save()
