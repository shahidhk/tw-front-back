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
        objs = list(ConstructionPhaseTbl.objects.filter(
            design_project=self.id))
        for obj in objs:
            new_obj = ProjectPhases()
            new_obj.__dict__ = obj.__dict__.copy()
            new_obj.start_date = obj.planned_date_range.lower
            new_obj.end_date = obj.planned_date_range.upper
            result.append(new_obj)
        return result

        # name=obj.name,
        # contract_number=obj.contract_number,
        # scope_description=obj.scope_description,
        # start_date=obj.planned_date_range.lower,
        # end_date=obj.planned_date_range.upper,
        # phase_number=obj.phase_number,
