# API calls are defined here
# See http://tw-confluence.duckdns.org/display/SAIS/Database for Docs
from djangoAPI.rest.serializers import ConstructionPhaseSerial, ProjectSerial, ProjectRoleSerial
from djangoAPI.models import DesignProjectHumanRoleTypeTbl, BusinessUnit

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import project


class ConstructionPhaseView(APIView):
    """
    blah blah blah this does some stuff
    """
    serializer_class = ConstructionPhaseSerial

    def get(self, request, proj_id, format=None):
        if proj_id == 0:
            phase = project.models.ConstructionPhases()
        else:
            phase = project.commons.construction_phase(proj_id)
        return render(request, 'blocks/construction-detailed.html', context={'phase': phase, })

    def post(self, request, phase_id=None, format=None):
        # Partial updates (partial=True) https://www.django-rest-framework.org/api-guide/serializers/#partial-updates
        # since operational bus unit should be inherited from super design project
        serializer = ConstructionPhaseSerial(data=request.data, partial=True)
        try:
            project_id = request.data['ic-current-url'].split('/')[-2]
        except Exception:
            return Response('Request had no referer', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            phases = project.commons.project_phases(project_id)  # todo project id
            return render(request, 'blocks/construction-phases.html', context={'phases': phases, })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveProjectView(APIView):
    """
    TODO
    """
    serializer_class = ProjectSerial

    def post(self, request, project_id, format=None):
        serializer = ProjectSerial(data=request.data)
        if serializer.is_valid():
            # project.commons.update_design_project(request, serializer.validated_data)
            details = project.commons.project_details(project_id)
            BUSINESS_UNITS = BusinessUnit.objects.all()
            return render(request, 'blocks/design-detailed.html', context={'proj': details, 'units': BUSINESS_UNITS})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProjectRoleView(APIView):
    """
    TODO
    """
    serializer_class = ProjectRoleSerial

    def get(self, request, proj_id, format=None):
        project_obj = project.commons.project_role(request, proj_id)
        AVAILABLE_ROLES = DesignProjectHumanRoleTypeTbl.objects.all()
        return render(request, 'blocks/project-role.html', context={'project': project_obj, 'roles': AVAILABLE_ROLES, })

    def post(self, request, format=None):
        serializer = ProjectRoleSerial(data=request.data)
        if serializer.is_valid():
            usr_id = request.user.id
            # update data here currently update_project_role does not do anything
            project.commons.update_project_role(usr_id, serializer)
            usr_projs = project.commons.user_projects(usr_id)
            return render(request, 'blocks/list-of-projects.html', context={'projects': usr_projs, })
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
