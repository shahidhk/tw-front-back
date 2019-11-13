from rest_framework import serializers
from django.http import JsonResponse, HttpResponse


class ProjectPhase(serializers.Serializer):
    """
    Serializer for phasing construction or design project phase information
    """
    phase_id = serializers.CharField(required=True)
    name = serializers.IntegerField(required=True)
    number = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Creates a new project phase
        """
        # use referrer for context
        # use id for more context
        return validated_data

    def update(self, instance, validated_data):
        """
        Updates existing project phase information
        """
        return validated_data


class RoleID(serializers.Serializer):
    role_id = serializers.IntegerField()


class DoesNotExistSerial(serializers.Serializer):
    role_id = serializers.IntegerField()
    entity_exists = serializers.BooleanField()


class AssetID(serializers.Serializer):
    asset_id = serializers.IntegerField()


class MissingRoleSerial(serializers.Serializer):
    role_number = serializers.CharField()
    role_name = serializers.CharField()
    parent_id = serializers.IntegerField()
    role_criticality = serializers.IntegerField()
    role_priority = serializers.IntegerField()
    role_spatial_site_id = serializers.IntegerField()


class MissingAssetSerial(serializers.Serializer):
    asset_serial_number = serializers.CharField()


class AssetRoleID(serializers.Serializer):
    role_id = serializers.IntegerField(allow_null=True)
    asset_id = serializers.IntegerField()


class BoolSerializer(serializers.Serializer):
    result = serializers.BooleanField()


class RoleParentID(serializers.Serializer):
    role_id = serializers.IntegerField()
    parent_id = serializers.IntegerField()
