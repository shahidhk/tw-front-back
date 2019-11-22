from django.db import models
from djangoAPI.models import ConstructionPhaseTbl, DesignProjectTbl, DesignProjectHumanRoleTypeTbl
# Dummy Models for serializers and graphene-django


class ProjectType():
    CONSTRUCTION = 'construction'
    DESIGN = 'design'
    PROJECT_TYPE = [(CONSTRUCTION, 'Construction'), (DESIGN, 'Design')]


class UserProjects(models.Model):
    """
    Model for list of User Projects
    """
    id = models.IntegerField(primary_key=True, null=False)
    project_number = models.CharField(max_length=100, null=False)
    project_name = models.CharField(max_length=200, null=False)
    user_role = models.ForeignKey(DesignProjectHumanRoleTypeTbl, models.DO_NOTHING, null=False)

    # DRF uses database tables to run validations so these tables need to acutally exist
    # class Meta:
    #     abstract = True


class ProjectDetails(DesignProjectTbl):
    """
    Model for details about the project
    """
    business_unit_name = models.CharField(max_length=200, null=True, blank=True)
    project_manager = models.CharField(max_length=200)
    project_manager_email = models.EmailField()
    key_bus_unit_contact = models.CharField(max_length=200)
    key_bus_unit_contact_email = models.EmailField()
    asset_data_steward = models.CharField(max_length=200)
    asset_data_steward_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()

    # class Meta:
    #     abstract = True


class ConstructionPhases(ConstructionPhaseTbl):
    """
    """
    start_date = models.DateField()
    end_date = models.DateField()
    # class Meta:
    #     abstract = True
