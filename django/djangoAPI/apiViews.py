# API calls are defined here
# See http://tw-confluence.duckdns.org/display/SAIS/Database for Docs
from .serializers import *
from .apiUtils import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


def ResultReturn(data):
    if data['result'] == 0:
        data = {'affected_rows': 1}
        return Response(data, status=status.HTTP_201_CREATED)
    elif data['result'] == 1:
        return Response(data['errors'], status=status.HTTP_409_CONFLICT)


class DevExplorationView(APIView):
    serializer_class = BoolSerializer

    def post(self, request):
        serializer = BoolSerializer(data=request.data)
        if serializer.is_valid():
            data = ExplorationUtil(serializer.data['result'])
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissingRole(APIView):
    serializer_class = MissingRoleSerial

    def post(self, request):
        serializer = MissingRoleSerial(data=request.data)
        if serializer.is_valid():
            data = MissingRoleUtil(serializer.data)
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissingAsset(APIView):
    serializer_class = MissingAssetSerial

    def post(self, request):
        serializer = MissingAssetSerial(data=request.data)
        if serializer.is_valid():
            data = MissingAssetUtil(serializer.data)
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignAssetToRole(APIView):
    serializer_class = AssetRoleID

    def post(self, request):
        serializer = AssetRoleID(data=request.data)
        if serializer.is_valid():
            data = AssignAssetToRoleUtil(serializer.data)
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntityExist(APIView):
    serializer_class = DoesNotExistSerial

    def post(self, request):
        serializer = DoesNotExistSerial(data=request.data)
        if serializer.is_valid():
            data = DoesNotExistUtil(serializer.data)
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetireAsset(APIView):
    serializer_class = AssetID

    def post(self, request):
        serializer = AssetID(data=request.data)
        if serializer.is_valid():
            data = RetireAssetUtil(serializer.data['asset_id'])
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleParent(APIView):
    serializer_class = RoleParentID

    def post(self, request):
        serializer = RoleParentID(data=request.data)
        if serializer.is_valid():
            data = RoleParentUtil(serializer.data)
            return ResultReturn(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
