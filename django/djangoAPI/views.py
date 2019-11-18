import csv
import os
import json
import random
import requests
import tarfile
import zipfile
import shutil
from uuid import uuid4
from datetime import date, timedelta

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.apps import apps
from django.db import transaction, connection
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoAPI.models import *
from djangoAPI.utils import num_to_alpha


def init_db2():
    '''
    Initilize the DB with extensions, views and ltree specific triggers
    '''
    with open('views.sql', 'r') as sql_file:
        queries = sql_file.read()
    queries = queries.split('!!!')
    with connection.cursor() as cursor:
        for query in queries:
            try:
                cursor.execute(query)
            except Exception as e:
                print(type(e))
                print(e)


def init_db(request):
    init_db2()
    return HttpResponse("Finished DB init")


def db_fill2():
    '''
    Fill the DB with test data
    Will eventually switch to initialization with constants for list tables
    '''
    init_value_lists()
    for i in range(4):
        obj = DesignProjectTbl.objects.create(
            pk=i + 1,
            name='design project phase name ' + str(i+1),
            designer_organization_name='designer organization name ' + str(i+1),
            phase_number=1,
            planned_date_range=(date.today(), date.today() + timedelta(days=40)),
            op_bus_unit_id=num_to_alpha(i+1),
            budget=1000000000.99,
            scope_description='this is a scope description',
        )

    lst = [['Super', 'User'], ['Tony', 'Huang'], ['Peter', 'Lewis'], ['Stephen', 'Almeida']]
    for i, value in enumerate(lst):
        usr = User.objects.create_user(
            value[0]+'.'+value[1], value[0]+'.'+value[1]+'@example.com', 'default')
        usr.last_name = value[1]
        usr.first_name = value[0]
        usr.save()
        obj = UserTbl.objects.create(
            pk=i + 1,
            auth_user_id=usr.pk,
            role_id=num_to_alpha(i+1),
            user_group_name_id=1,
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
            num = str(uuid4())
            print(num)
            ConstructionPhaseTbl.objects.create(
                pk=i*3+j,
                name='project construction phase ' + str(i*3+j),
                planned_date_range=(today-timedelta(days=15), today),
                phase_number=i,
                design_project_id=j + 1,
                scope_description='a project construction phase',
                op_bus_unit_id=['a', 'b', 'c'][i],
                constructor_organization_name='construction company, hopefully not snc lavalin',
                contract_number=num,
                budget=10000000.68
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
    for tbl in DBTbls.objects.all():
        for usr in AllHumanRoleTypeTbl.objects.all():
            AccessProfileDefinitionTbl.objects.create(
                db_table=tbl,
                role=usr,
                permission_to_view=True,
                permission_to_update=True
            )
    for i in range(3):
        for j in range(3):
            UserProjectLinkTbl.objects.create(
                project_id=j+2,
                title_id='a',
                user_id=i+2,
            )

    asset_line = {}
    with open('avantis.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count = line_count + 1
            asset_line[row[0]] = [line_count, row]

    # create a location for states
    spatial_state = ImportedSpatialSiteTbl.objects.create(
        pk=1,
        name='Virtual Spatial Location for States',
    )
    with connection.cursor() as cursor:
        cursor.execute("""SELECT setval(pg_get_serial_sequence('"djangoAPI_ImportedSpatialSiteTbl"','spatial_site_id'), coalesce(max("spatial_site_id"), 1), max("spatial_site_id") IS NOT null) FROM "djangoAPI_ImportedSpatialSiteTbl";""")

    # create spatial sites
    locations = {}
    for asset_row in asset_line.items():
        if not locations.get(asset_row[1][1][7]):
            spatial_site = ImportedSpatialSiteTbl.objects.create(
                name=asset_row[1][1][7]
            )
            locations[asset_row[1][1][7]] = [spatial_site.pk, asset_row[1][1][3], spatial_site]
    for location in locations.values():
        temp = asset_line.get(location[1])
        if temp:
            temp = locations.get(temp[1][7])
            spatial_site = location[2]
            if temp:
                spatial_site.parent_site_id_id = temp[0]
                spatial_site.save()

    # create our state roles
    states = ['Top Level Roles', 'Orphaned Roles']
    for i in range(10):
        name = MasterRoleNumbersTbl.objects.create(
            role_number='State ' + str(i+1),
            project_tbl_id=1
        )
        role = ProjectAssetRoleRecordTbl.objects.create(
            pk=i + 1,
            updatable_role_number=name,
            role_name=states[i] if i < len(states) else 'Reserved for Future State',
            parent_id_id=None,
            role_criticality_id='a',
            role_priority_id='a',
            role_spatial_site_id_id='1',
            project_tbl_id=1,
        )
    with connection.cursor() as cursor:
        cursor.execute("""SELECT setval(pg_get_serial_sequence('"djangoAPI_ProjectAssetRoleRecordTbl"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "djangoAPI_ProjectAssetRoleRecordTbl";""")

    for asset_row in asset_line.items():
        name = MasterRoleNumbersTbl.objects.create(
            role_number=asset_row[0]
        )

        avantis_asset = ClonedAssetAndRoleInRegistryTbl.objects.create(
            mtoi=asset_row[1][0],
            role_number=asset_row[0],
            role_name=asset_row[1][1][1],
            parent_role_number=asset_row[1][1][3],
            role_location=asset_row[1][1][7],
            role_criticality=asset_row[1][1][6],
            role_priority=5,  # did not exist in my avantis import
            role_equipment_type='meh',
            role_classification='does this even matter right now?',
            asset_serial_number='dont have this value either',
            suspension_id=1,
            already_reserved_id=1,
            intent_to_reserve_id=1,
        )


def db_fill(request):
    db_fill2()
    return HttpResponse("Finished DB Fill")


def update_asset_role2():
    cloned_assets = ClonedAssetAndRoleInRegistryTbl.objects.all()
    parent_mtoi = {}  # dictionary for quickly finding entry by role number
    for entry in cloned_assets:  # populate dict, keys = role number
        if entry.role_number in parent_mtoi.keys():
            pass
        else:
            parent_mtoi[entry.role_number] = entry
    role_numbers = MasterRoleNumbersTbl.objects.in_bulk(field_name='role_number')
    base_role_dict = {}  # dictionary for tracking roles and its pk
    with transaction.atomic():
        for entry in cloned_assets:
            existing_role = PreDesignReconciledRoleRecordTbl.objects.create(
                updatable_role_number=role_numbers[entry.role_number],
                role_name=entry.role_name,
                parent_id_id=None,  # fill this in on the second go
                role_criticality_id=num_to_alpha(entry.role_criticality),
                role_priority_id=num_to_alpha(entry.role_priority),
                role_spatial_site_id_id=1,  # TODO this is obviously a placeholder
                cloned_role_registry_tbl_id=parent_mtoi[entry.role_number].mtoi,
                entity_exists=True,
                missing_from_registry=False,
                designer_planned_action_type_tbl_id=num_to_alpha(3),  # do nothing
                parent_changed=False,
            )
            base_role_dict[entry.role_number] = existing_role.pk
    base_roles = ProjectAssetRoleRecordTbl.objects.all()
    # with transaction.atomic():
    for role in base_roles:
        try:  # update the parent of roles unless its top level in which case it is suppose to be child of 1
            role.parent_id_id = base_role_dict.get(
                parent_mtoi[role.updatable_role_number.role_number].parent_role_number, 1)
            role.save()
        except Exception as e:
            print('cant save parent for ' +
                  role.updatable_role_number.role_number + str(type(e)) + str(e))
        else:
            print('saved parent for ' + role.updatable_role_number.role_number)
    # populate predesign asset records
    with transaction.atomic():
        for entry in cloned_assets:
            existing_asset = PreDesignReconciledAssetRecordTbl()
            existing_asset.asset_serial_number = 'ASN ' + entry.role_number
            existing_asset.cloned_role_registry_tbl_id = parent_mtoi[entry.role_number].mtoi
            existing_asset.initial_project_asset_role_id_id = base_role_dict[entry.role_number]
            existing_asset.entity_exists = True
            existing_asset.missing_from_registry = False
            existing_asset.designer_planned_action_type_tbl_id = num_to_alpha(3)  # do nothing
            existing_asset.role_changed = False
            existing_asset.save()


def update_asset_role(request):
    update_asset_role2()
    return HttpResponse('Finished Updating Asset & Role')


def test(request):
    message = Mail(
        from_email='amber.brasher@toronto.ca',
        to_emails='jon.ma@toronto.ca',
        subject='Meeting with Annette',
        html_content='<strong>Annette is holding me hostage in the Taylor-Massey Creek meetin room</strong>')
    try:
        sg = SendGridAPIClient(
            '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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        return HttpResponse(response.headers)
    except Exception as e:
        return HttpResponse('error ' + str(e))


def init_all(request):
    with transaction.atomic():
        init_db2()
        db_fill2()
        update_asset_role2()
        User.objects.create_superuser('jma', 'jma@toronto.ca', 'tw-admin')
    with open('reset_sequence.sql', 'r') as sql_file:
        query = sql_file.read()
    with connection.cursor() as cursor:
        cursor.execute(query)
    subdomain = os.getenv('BRANCH', '')
    tables = ['reconciliation_view', 'orphan_view', 'reservation_view', 'unassigned_assets',
              'garbage_can_unassigned_assets', 'garbage_can_reconciliation_view']
    for table in tables:
        response = requests.post(
            'https://hasura.' + subdomain + '.duckdns.org/v1/query',
            json={
                "type": "track_table",
                "args": {
                    "table": {
                        "schema": "public",
                        "name": table
                    }
                }
            },
            headers={'x-hasura-admin-secret': 'eDfGfj041tHBYkX9'}
        )
        if response.json()['message'] != 'success':
            print('Track ' + table + ' failed!')
            print(response.json())

    response = requests.post(
        'https://hasura.' + subdomain + '.duckdns.org/v1/query',
        json={
            "type": "add_remote_schema",
            "args": {
                "name": "django",
                "definition": {
                    "url": "https://django." + subdomain + ".duckdns.org/graphql/",
                    # "headers": [{"name": "X-Server-Request-From", "value": "Hasura"}],
                    "forward_client_headers": True,
                    "timeout_seconds": 60
                },
            },
        },
        headers={'x-hasura-admin-secret': 'eDfGfj041tHBYkX9'}
    )
    if response.json()['message'] != 'success':
        print('Add Remote Schema failed!')
        print(response.json())
    return HttpResponse('Finished All Init Actions')


def update_webapp(request):
    """Fetches the Latest Build from Github"""
    access_token = os.getenv('GITHUB_TOKEN', '7884e5f1f3d276fbc68a41dffb2d6149bde849e6')
    response = requests.get(
        'https://api.github.com/repos/abrasher/tw-webapp/releases?access_token='+access_token,
    )
    try:
        new_url = response.json()[0]['assets'][0]['url']
    except Exception:
        return HttpResponse(response.json())
    else:
        print(new_url)
        response = requests.get(
            new_url+'?access_token='+access_token,
            headers={'Accept': 'application/octet-stream'},
        )
        open('./webapp/release.zip.tgz', 'wb').write(response.content)
        if os.path.exists('./webapp/dist'):
            shutil.rmtree('./webapp/dist/')
        tgz = tarfile.open('./webapp/release.zip.tgz')
        tgz.extractall('./webapp')
        tgz.close()
        tgz = zipfile.ZipFile('./webapp/release.zip')
        tgz.extractall('./webapp')
        tgz.close()
        os.remove('./webapp/release.zip.tgz')
        os.remove('./webapp/release.zip')
        return HttpResponse('finished downloading latest release')
