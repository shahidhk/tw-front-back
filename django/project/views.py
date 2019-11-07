from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from djangoAPI.models import *
from project.commons import *
# Create your views here.


@login_required
def UserProjects(request):
    """Display all projects that are the user belongs to"""
    usr_id = request.user.id
    usr_obj = UserTbl.objects.get(pk=usr_id)
    usr_projs = []
    # the role_id in *HumanRoleTypeTbl is the same for all tables so it can be used to find both design and construction projects human roles
    design_proj_roles = DesignProjectHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for design_proj_role in design_proj_roles:
        design_proj = DesignProjectTbl.objects.get(pk=design_proj_role.design_project_id)
        usr_role = DesignProjectHumanRoleTypeTbl.objects.get(pk=design_proj_role.human_role_type_id)
        display_proj = DisplayUserProjects(design_proj.id, design_proj.name, usr_role.name)
        usr_projs.append(display_proj)
    constr_proj_roles = ConstructionPhaseHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for constr_proj_role in constr_proj_roles:
        constr_proj = ConstructionPhaseTbl.objects.get(pk=constr_proj_role.design_project_id)
        usr_role = ConstructionPhaseHumanRoleTypeTbl.objects.get(
            pk=constr_proj_role.human_role_type_id)
        display_proj = DisplayUserProjects(constr_proj.id, constr_proj.name, usr_role.name)
        usr_projs.append(display_proj)
    return render(request, 'user_projects.html', context={'projects': usr_projs, })
