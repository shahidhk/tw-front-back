from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from djangoAPI.models import *
from project.forms import *
import project.commons
# Create your views here.


def project_home(request):
    """
    Display all projects that are the user belongs to
    """
    if not request.user.is_authenticated:
        return render(request, 'project-home.html')
    usr_id = request.user.id
    usr_projs = project.commons.user_projects(usr_id)
    return render(request, 'project-user.html', context={'projects': usr_projs, })


def project_details(request, proj_id):
    """
    Display the Details of a Project
    """
    details = project.commons.project_details(proj_id)
    phases = project.commons.project_phases(proj_id)
    print(vars(details))
    return render(request, 'project-detail.html', context={'proj': details, 'phases': phases})


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
