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


def init_db(request):
    '''
    Initilize the DB with extensions, views and ltree specific triggers
    '''
    with connection.cursor() as cursor:
        cursor.execute('CREATE EXTENSION ltree;')
        cursor.execute('''ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl" DROP COLUMN ltree_path;
        ALTER TABLE public."djangoAPI_ProjectAssetRoleRecordTbl"
            ADD COLUMN ltree_path ltree;
        CREATE INDEX parent_id_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" USING GIST (ltree_path);
        CREATE INDEX parent_path_idx ON public."djangoAPI_ProjectAssetRoleRecordTbl" (parent_id_id);''')
        cursor.execute(
            '''
        CREATE OR REPLACE FUNCTION update_parent_path() RETURNS TRIGGER AS $$
            DECLARE
                path ltree;
            BEGIN
                IF NEW.parent_id_id IS NULL THEN
                    NEW.ltree_path = 'root'::ltree;
                ELSEIF TG_OP = 'INSERT' OR OLD.parent_id_id IS NULL OR OLD.parent_id_id != NEW.parent_id_id THEN
                    SELECT ltree_path || id::text FROM public."djangoAPI_ProjectAssetRoleRecordTbl" WHERE id = NEW.parent_id_id INTO path;
                    IF path IS NULL THEN
                        RAISE EXCEPTION 'Invalid parent_id %. Entities must be added parents first', NEW.parent_id_id;
                    END IF;
                    NEW.ltree_path = path;
                    UPDATE public."djangoAPI_ProjectAssetRoleRecordTbl"
                        SET ltree_path = path || subpath(ltree_path,nlevel(OLD.ltree_path)) WHERE ltree_path <@ OLD.ltree_path AND ltree_path != OLD.ltree_path;
                END IF;
                RETURN NEW;
            END;
        $$ LANGUAGE plpgsql;
        ''')
        cursor.execute(
            '''
        CREATE TRIGGER parent_path_tgr
            BEFORE INSERT OR UPDATE ON public."djangoAPI_ProjectAssetRoleRecordTbl"
            FOR EACH ROW EXECUTE PROCEDURE update_parent_path();
        ''')
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
        where pa.initial_project_asset_role_id_id is null and pa.designer_planned_action_type_tbl_id<>2;
        ''')
        return HttpResponse("Finished DB Fill")


def db_fill(request):
    '''
    Fill the DB with test data
    Will eventually switch to initialization with constants for list tables
    '''
    for i in range(2):
        i = i + 1
        OperationalBusinessUnit.objects.create(
            pk=i,
            name='OpBusUnit Number ' + str(i),
        )
    for i in range(10):
        Sites.objects.create(
            pk=i+1,
            site_id='ST' + str(i),
            site_name='Site ' + str(i),
            op_bus_unit_id=i/5+1,
        )
    for i in range(5):
        DesignStageTypeTbl.objects.create(
            pk=i+1,
            name='Design Stage Type ' + str(i+1),
        )
    lst = ['move', 'dispose', 'nothing']
    j = 1
    for i in lst:
        DesignerPlannedActionTypeTbl.objects.create(
            pk=j,
            name=i,
        )
        j = j + 1
    for i in range(5):
        RoleCriticality.objects.create(
            id=i+1,
        )
    for i in range(5):
        RolePriority.objects.create(
            id=i+1,
        )
    lst = ['Tony Huang', 'Peter Lewis', 'Stephen Almeida']
    j = 0
    for i in lst:
        ProjectTbl.objects.create(
            pk=j+1,
            project_manager=i,
            date_range=(date.today(), date.today() + timedelta(days=40)),
            project_site_id=random.randint(1, 2),
        )
        j = j + 1
    today = date.today()
    for i in range(2):
        today = today + timedelta(days=5)
        for j in range(3):
            ProjectDesignPhaseTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=5), today),
                project_design_stage_type_id=random.randint(1, 5),
                project_tbl_id=j + 1,
            )
    today = date.today() + timedelta(days=10)
    for i in range(2):
        today = today + timedelta(days=15)
        for j in range(3):
            ProjectConstructionPhaseTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=15), today),
                phase_number=i,
                project_tbl_id=j + 1,
            )
    today = date.today() + timedelta(days=10)
    for i in range(2):
        today = today + timedelta(days=5)
        for j in range(3):
            ProjectConstructionStageTbl.objects.create(
                pk=i*3+j,
                planned_date_range=(today-timedelta(days=5), today),
                project_construction_phase_id=i+1,
                project_construction_stage_type_id=random.randint(1, 5),
            )
    asset_line = {}
    with open('hashed_entities.csv', mode='r') as csv_file:
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
        avantis_asset.mtnoi = asset_row[1][0]
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
    parent_mtnoi = {}  # dictionary for quickly finding entry by role number
    result_str = ''  # string for errors
    for entry in cloned_assets:  # populate dict, keys = role number
        if entry.role_number in parent_mtnoi.keys():
            result_str = result_str + entry.role_number + \
                ' has duplicates in the cloned table\n'
        else:
            parent_mtnoi[entry.role_number] = entry
    base_role_dict = {}  # dictionary for tracking roles and its pk

    # base_roles = projectAssetRoleRecordTbl.objects.all()
    # for role in base_roles:
    #     base_role_dict[role.updatable_role_number] = role.pk

    # create project asset role record table
    with transaction.atomic():
        for entry in cloned_assets:
            existing_role = PreDesignReconciledRoleRecordTbl()
            existing_role.updatable_role_number = entry.role_number
            existing_role.role_name = entry.role_name
            existing_role.parent_id_id = None  # fill this in on the second go
            existing_role.role_criticality_id = entry.role_criticality
            existing_role.role_priority_id = entry.role_priority
            existing_role.role_spatial_site_id = entry.role_spatial_site_id
            existing_role.cloned_role_registry_tbl_id = parent_mtnoi[entry.role_number].mtnoi
            existing_role.entity_exists = True
            existing_role.missing_from_registry = False
            existing_role.designer_planned_action_type_tbl_id = 3  # do nothing
            existing_role.save()
            base_role_dict[existing_role.updatable_role_number] = existing_role.pk
    base_roles = ProjectAssetRoleRecordTbl.objects.all()
    with transaction.atomic():
        for role in base_roles:
            try:
                role.parent_id_id = base_role_dict[parent_mtnoi[role.updatable_role_number].parent_role_number]
                role.save()
            except Exception:
                print(
                    parent_mtnoi[role.updatable_role_number].parent_role_number)
    # populate predesign asset records
    with transaction.atomic():
        for entry in cloned_assets:
            existing_asset = PreDesignReconciledAssetRecordTbl()
            existing_asset.asset_serial_number = 'disguised asset serial number'
            existing_asset.cloned_role_registry_tbl_id = parent_mtnoi[entry.role_number].mtnoi
            existing_asset.initial_project_asset_role_id_id = base_role_dict[entry.role_number]
            existing_asset.entity_exists = True
            existing_asset.missing_from_registry = False
            existing_asset.designer_planned_action_type_tbl_id = 3  # do nothing
            existing_asset.save()
    return HttpResponse(result_str + 'Finished Updating Asset & Role')


def test(request):
    base_assets = PreDesignReconciledAssetRecordTbl.objects.all()
    with transaction.atomic():
        for asset in base_assets:
            asset.asset_serial_number = 'role # ' + \
                str(asset.initial_project_asset_role_id_id) + \
                'asset serial number'
            asset.save()
