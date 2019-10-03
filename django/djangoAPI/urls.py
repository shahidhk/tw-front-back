from django.urls import path
from . import views

urlpatterns = [
    path('initdb/', views.init_db),
    path('filldb/', views.db_fill),
    path('updatedb/', views.update_asset_role),
    path('test/', views.test),
]
