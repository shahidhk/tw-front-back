from django.db import models
from djangoAPI.models import *

# Create your models here.
# these models will be used to create and validate forms which do not actually exist in the db

# class ProjectDetails(models.Model):
#     """
#     Model for project information view
#     """

#     business_unit = models.ForeignKey(BusinessUnit, models.DO_NOTHING)
#     design_contract_number = models.CharField(max_length=100)
#     # design_project_manager = models.ForeignKey

#     class Meta:
#         managed = False
#         db_table = "does_not_exist"
