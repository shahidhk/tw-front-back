import graphene
from django.db import models
from graphene_django.types import DjangoObjectType

from djangoAPI.models import *
from project.models import UserProjects, ProjectDetails, ProjectPhases, ProjectType

# graphene classes using models


class ProjectPhasesType(DjangoObjectType):
    class Meta:
        model = ProjectPhases


class UsersProjectsType(DjangoObjectType):
    class Meta:
        model = UserProjects


class ProjectDetailsType(DjangoObjectType):
    project_phases = graphene.List(graphene.NonNull(ProjectPhasesType))
    # project_phases = graphene.String()

    class Meta:
        model = ProjectDetails

    def resolve_project_phases(self, info):
        result = []
        objs = list(DesignStageTbl.objects.filter(
            design_project=self.id).order_by('planned_date_range'))
        for obj in objs:
            result.append(
                ProjectPhases(
                    name="placeholder name",
                    contract_number="placeholder contract number",
                    scope_description="place holder description",
                )
            )
        return result
