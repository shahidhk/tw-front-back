from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from djangoAPI.models import *
from project.commons import *
from project.forms import *
# Create your views here.


def project_home(request):
    """
    Display all projects that are the user belongs to
    """
    if not request.user.is_authenticated:
        return render(request, 'project-home.html')
    usr_id = request.user.id
    usr_obj = UserTbl.objects.get(pk=usr_id)
    usr_projs = []
    # the role_id in *HumanRoleTypeTbl is the same for all tables so it can be used to find both design and construction projects human roles
    design_proj_roles = DesignProjectHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for design_proj_role in design_proj_roles:
        design_proj = DesignProjectTbl.objects.get(pk=design_proj_role.design_project_id)
        usr_role = DesignProjectHumanRoleTypeTbl.objects.get(pk=design_proj_role.human_role_type_id)
        display_proj = DisplayUserProjects(
            design_proj.id, design_proj.name, usr_role.name, 'design')
        usr_projs.append(display_proj)
    constr_proj_roles = ConstructionPhaseHumanRoleTbl.objects.filter(
        human_role_type_id=usr_obj.role_id)
    for constr_proj_role in constr_proj_roles:
        constr_proj = ConstructionPhaseTbl.objects.get(pk=constr_proj_role.construction_phase_id)
        usr_role = ConstructionPhaseHumanRoleTypeTbl.objects.get(
            pk=constr_proj_role.human_role_type_id)
        display_proj = DisplayUserProjects(
            constr_proj.id, constr_proj.name, usr_role.name, 'construction')
        usr_projs.append(display_proj)
    return render(request, 'project-user.html', context={'projects': usr_projs, })


def project_details(request, proj_type, proj_id):
    """
    Display the Details of a Project

    The Project can be Construction or Design
    """
    if proj_type == 'design':
        proj = get_object_or_404(DesignProjectTbl, pk=proj_id)
        disp_proj_detail = DisplayProjectDetails(
            bus_unit=proj.op_bus_unit.name,
            design_contract_number=proj.contract_number,
            project_scope_description=proj.scope_description,
            start_date=proj.planned_date_range.lower,
        )
        phases = list(DesignStageTbl.objects.filter(
            design_project=proj).order_by('planned_date_range'))
        proj_type = 'Design'
    elif proj_type == 'construction':
        proj = get_object_or_404(ConstructionPhaseTbl, pk=proj_id)
        disp_proj_detail = DisplayProjectDetails(
            bus_unit=proj.op_bus_unit.name,
            design_contract_number=proj.contract_number,
            project_scope_description=proj.scope_description,
            start_date=proj.planned_date_range.lower,
        )
        phases = list(ConstructionStageTbl.objects.filter(
            construction_phase=proj).order_by('planned_date_range'))
        proj_type = 'Construction'
    else:
        raise Http404(proj_type + ': Project Type Does Not Exist')
    return render(request, 'project-detail.html', context={'proj': disp_proj_detail, 'phases': phases, 'type': proj_type, })


def project_edit(request, obj_id=None):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = DesignProjectForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('project-details'))

    # If this is a GET (or any other method) create the default form.
    else:
        if obj_id:
            obj = get_object_or_404(DesignProjectTbl, pk=obj_id)
            form = DesignProjectForm(instance=obj)
        else:
            form = DesignProjectForm()
    context = {
        'form': form,
    }

    return render(request, 'generic-form.html', context)


class DesignProjectCreate(CreateView):
    template_name = 'generic-form.html'
    model = DesignProjectTbl
    fields = '__all__'
    success_url = reverse_lazy('project-details')
