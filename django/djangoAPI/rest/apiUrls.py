from django.urls import path

from djangoAPI.rest.apiViews import *

urlpatterns = [
    path("api/save-phase/", ConstructionPhaseView.as_view(), name="save_phase"),
    path("api/save-project/", SaveProjectView.as_view(), name="save_project"),
    path("api/update-role/", ChangeProjectRoleView.as_view(), name="update_project_role"),
    path("api/construction-detailed/<int:proj_id>/", ConstructionPhaseView.as_view(), name="construction_detailed"),
]
