import graphene
from django.db import models
from graphene_django.types import DjangoObjectType

from djangoAPI.models import *
from project.models import UserProjects, ProjectDetails, ConstructionPhases, ProjectType

# graphene classes using models


class ProjectPhasesType(DjangoObjectType):
    id = graphene.Int()  # there is a weird bug where graphene does not return the id so we will just explicitly define it

    class Meta:
        model = ConstructionPhases
        exclude = ('planned_date_range',)

    def resolve_id(self, info):
        return self.id


class UsersProjectsType(DjangoObjectType):
    class Meta:
        model = UserProjects


class ProjectDetailsType(DjangoObjectType):
    project_phases = graphene.List(graphene.NonNull(ProjectPhasesType))
    id = graphene.Int()

    class Meta:
        model = ProjectDetails
        exclude = ('planned_date_range',)

    def resolve_id(self, info):
        return self.id

    def resolve_project_phases(self, info):
        result = []
        objs = list(ConstructionPhaseTbl.objects.filter(
            design_project=self.id))
        for obj in objs:
            new_obj = ProjectPhasesType()
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
