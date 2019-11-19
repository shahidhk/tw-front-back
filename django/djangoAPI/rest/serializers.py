from rest_framework import serializers
from django.http import JsonResponse, HttpResponse
from project.models import UserProjects, ConstructionPhases, ProjectDetails


class ConstructionPhaseSerial(serializers.ModelSerializer):
    """
    Serializer for phasing construction or design project phase information
    """
    class Meta:
        model = ConstructionPhases
        fields = '__all__'

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


class ProjectSerial(serializers.Serializer):
    """
    Serializer for ..
    """
    class Meta:
        model = ProjectDetails
        fields = '__all__'

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
