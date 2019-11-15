from django.db import models
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
    user_role = models.CharField(max_length=50, null=False)

    class Meta:
        abstract = True


class ProjectDetails(models.Model):
    """
    Model for details about the project
    """
    id = models.IntegerField(primary_key=True, null=False)
    bus_unit = models.CharField(max_length=200, null=False, primary_key=True)
    design_contract_number = models.CharField(max_length=200, null=False)
    project_manager = models.CharField(max_length=200)
    project_manager_email = models.EmailField()
    key_bus_unit_contract = models.CharField(max_length=200)
    key_bus_unit_contract_email = models.EmailField()
    asset_data_steward = models.CharField(max_length=200)
    asset_data_steward_email = models.EmailField()
    project_scope_description = models.TextField()
    start_date = models.DateField(null=False)

    class Meta:
        abstract = True


class ProjectPhases(models.Model):
    """
    """
    name = models.CharField(max_length=200, null=False)
    contract_number = models.CharField(max_length=50, null=True)
    scope_description = models.TextField(null=False)
    project = models.ForeignKey(ProjectDetails, models.DO_NOTHING, null=False)

    class Meta:
        abstract = True
