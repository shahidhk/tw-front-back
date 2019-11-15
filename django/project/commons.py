import datetime
from dataclasses import dataclass, field
from djangoAPI.models import *
from project.models import *
from djangoAPI.graphql.projects import *
from django.shortcuts import render, get_object_or_404


@dataclass(order=True)
class DisplayUserProjects:
    """
    Simple Class for displaying which projects a user belongs to
    """
    project_number: str = ''
    project_name: str = ''
    user_role: str = ''
    project_type: str = ''


@dataclass(order=True)
class DisplayProjectDetails:
    """
    Class for Passing Project Detailed information to template
    """
    bus_unit: str = ''
    design_contract_number: str = ''
    project_manager: str = ''
    project_manager_email: str = ''
    key_bus_unit_contract: str = ''
    key_bus_unit_contract_email: str = ''
    asset_data_steward: str = ''
    asset_data_steward_email: str = ''
    project_scope_description: str = ''
    start_date: datetime.date = datetime.date.today()


def user_projects(usr_id):
    """
    Display all projects that are the user belongs to
    Returns 
    """
    usr_obj = UserTbl.objects.get(pk=usr_id)
    usr_projs = []
    # the role_id in *HumanRoleTypeTbl is the same for all tables so it can be used to find both design and construction projects human roles
    design_proj_roles = DesignProjectHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for design_proj_role in design_proj_roles:
        design_proj = DesignProjectTbl.objects.get(pk=design_proj_role.design_project_id)
        usr_role = DesignProjectHumanRoleTypeTbl.objects.get(pk=design_proj_role.human_role_type_id)
        display_proj = UserProjects(design_proj.id, design_proj.id,
                                    design_proj.name, usr_role.name, 'design')
        usr_projs.append(display_proj)
    constr_proj_roles = ConstructionPhaseHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for constr_proj_role in constr_proj_roles:
        constr_proj = ConstructionPhaseTbl.objects.get(pk=constr_proj_role.construction_phase_id)
        usr_role = ConstructionPhaseHumanRoleTypeTbl.objects.get(
            pk=constr_proj_role.human_role_type_id)
        display_proj = UserProjects(constr_proj.id, constr_proj.id,
                                    constr_proj.name, usr_role.name, 'construction')
        usr_projs.append(display_proj)
    return usr_projs


def project_details(proj_type, proj_id):
    """
    Display the Details of a Project

    The Project can be Construction or Design
    """
    if proj_type == 'design':
        proj = get_object_or_404(DesignProjectTbl, pk=proj_id)
        disp_proj_detail = ProjectDetails(
            proj_id=proj_id,
            project_type=ProjectType.DESIGN,
            bus_unit=proj.op_bus_unit.name,
            design_contract_number=proj.contract_number,
            project_scope_description=proj.scope_description,
            start_date=proj.planned_date_range.lower,
        )
    elif proj_type == 'construction':
        proj = get_object_or_404(ConstructionPhaseTbl, pk=proj_id)
        disp_proj_detail = ProjectDetails(
            proj_id=proj_id,
            project_type=ProjectType.CONSTRUCTION,
            bus_unit=proj.op_bus_unit.name,
            design_contract_number=proj.contract_number,
            project_scope_description=proj.scope_description,
            start_date=proj.planned_date_range.lower,
        )
    else:
        raise Exception(proj_type + ': Project Type Does Not Exist')
    return [disp_proj_detail]
