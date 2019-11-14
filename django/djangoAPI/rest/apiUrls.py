from django.urls import path

from djangoAPI.rest.apiViews import *

urlpatterns = [
    path("api/save-phase/", SavePhaseView.as_view(), name="save_phase"),
    path("api/save-project/", SaveProjectView.as_view(), name="save_project"),
]
