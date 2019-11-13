# API calls are defined here
# See http://tw-confluence.duckdns.org/display/SAIS/Database for Docs
from djangoAPI.rest.serializers import *
# from djangoAPI.rest.apiUtils import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class SavePhaseView(APIView):
    """
    blah blah blah this does some stuff
    """
    serializer_class = ProjectPhase

    def post(self, request, format=None):
        serializer = ProjectPhase(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
