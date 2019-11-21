from django.urls import path

from djangoAPI.rest.apiViews import *

urlpatterns = [
    path("api/save-phase/<int:phase_id>/", ConstructionPhaseView.as_view(), name="save_phase"),
    path("api/save-phase/None/", ConstructionPhaseView.as_view(), name="new_phase"),
    path("api/save-project/<int:project_id>/", SaveProjectView.as_view(), name="save_project"),
    path("api/update-role/", ChangeProjectRoleView.as_view(), name="update_project_role"),
    path("api/project-role/<int:proj_id>/", ChangeProjectRoleView.as_view(), name="get_project_role"),
    path("api/construction-detailed/<int:proj_id>/",
         ConstructionPhaseView.as_view(), name="construction_detailed"),
]
