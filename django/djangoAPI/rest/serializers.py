from rest_framework import serializers
from django.http import JsonResponse, HttpResponse
from project.models import UserProjects, ConstructionPhases, ProjectDetails
from djangoAPI.models import DesignProjectTbl


class DesignProjectSerial(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = DesignProjectTbl
        fields = '__all__'


class ConstructionPhaseSerial(serializers.ModelSerializer):
    """
    Serializer for phasing construction or design project phase information
    """
    contract_number = serializers.CharField(required=True)

    class Meta:
        model = ConstructionPhases
        fields = '__all__'

    def validate_contract_number(self, value):
        print('VALIDATING CONTRACT NUMBER')
        if not value:
            raise serializers.ValidationError("contract number is invalid")
        return value

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


class ProjectSerial(serializers.ModelSerializer):
    """
    Serializer for ..
    """
    class Meta:
        model = ProjectDetails
        fields = '__all__'
        # exclude = ['super_design_project', 'op_bus_unit', ]
        # depth = 10

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


class ProjectRoleSerial(serializers.ModelSerializer):
    class Meta:
        model = UserProjects
        fields = '__all__'

    def create(self, validated_data):
        """
        TODO
        """
        return validated_data

    def save(self, **kwargs):
        print(kwargs)
        return None
