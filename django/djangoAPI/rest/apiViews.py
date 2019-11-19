# API calls are defined here
# See http://tw-confluence.duckdns.org/display/SAIS/Database for Docs
from djangoAPI.rest.serializers import *
# from djangoAPI.rest.apiUtils import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import project.commons


class ConstructionPhaseView(APIView):
    """
    blah blah blah this does some stuff
    """
    serializer_class = ConstructionPhaseSerial

    def get(self, request, proj_id, format=None):
        phase = project.commons.construction_phase(proj_id)
        return render(request, 'blocks/construction-detailed.html', context={'phase': phase, })

    def post(self, request, format=None):
        # Partial updates (partial=True) https://www.django-rest-framework.org/api-guide/serializers/#partial-updates
        serializer = ConstructionPhaseSerial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveProjectView(APIView):
    """
    TODO
    """
    serializer_class = ProjectSerial

    def post(self, request, format=None):
        serializer = ProjectSerial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProjectRoleView(APIView):
    """
    TODO
    """

    serializer_class = ProjectRoleSerial

    def post(self, request, format=None):
        serializer = ProjectRoleSerial(data=request.data)
        if serializer.is_valid():
            usr_id = request.user.id
            usr_projs = project.commons.user_projects(usr_id)
            return render(request, 'blocks/list-of-projects.html', context={'projects': usr_projs, })
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
