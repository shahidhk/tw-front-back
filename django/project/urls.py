from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.project_home, name='project-home'),
    path('details/<int:proj_id>/', views.project_details, name='project-details'),
    path('edit-project/', views.project_edit, name='project-edit'),
    path('edit-project/<int:obj_id>', views.project_edit, name='project-update'),
    path('edit-generic', views.DesignProjectCreate.as_view()),
    # path('', TemplateView.as_view(template_name='project-home.html'), name='project-home'),
]
