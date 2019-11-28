import os
import shutil
import tarfile
import zipfile

import requests
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from djangoAPI.initialize import (clean_up_incrementers,
                                  fill_database_test_data, parse_avantis_data,
                                  run_sql_scripts, update_hasura_schema)


def init_db(request):
    run_sql_scripts()
    return HttpResponse("Finished DB init")


def db_fill(request):
    fill_database_test_data()
    return HttpResponse("Finished DB Fill")


def update_asset_role(request):
    parse_avantis_data()
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
        run_sql_scripts()
        fill_database_test_data()
        parse_avantis_data()
        User.objects.create_superuser('jma', 'jma@toronto.ca', 'tw-admin')
    clean_up_incrementers()
    update_hasura_schema()
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


def get_webapp(request):
    tag = request.GET.get('tag')
    access_token = os.getenv('GITHUB_TOKEN', '7884e5f1f3d276fbc68a41dffb2d6149bde849e6')
    response = requests.get(
        'https://api.github.com/repos/abrasher/tw-webapp/releases/tags/'+tag+'?access_token='+access_token,
    )
    try:
        new_url = response.json()['assets'][0]['url']
    except Exception:
        return HttpResponse(str(response.json()) + ' : '+response.url)
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
