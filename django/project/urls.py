from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('home/', views.UserProjects, name='user-projects'),
    path('', TemplateView.as_view(template_name='project-home.html'), name='project-home'),
]
