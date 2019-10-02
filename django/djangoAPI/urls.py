from django.urls import path
from . import views

urlpatterns = [
    path('initdb/', views.db_init, name='init_db'),
    path('filldb/', views.update_asset_role),
    path('test/', views.test),
]