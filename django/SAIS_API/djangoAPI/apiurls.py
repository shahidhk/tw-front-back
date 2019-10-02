from django.urls import path

from .apiViews import *

urlpatterns = [
    path("api/missing-role/", MissingRole.as_view(), name="missing_role"),
    path("api/missing-asset/", MissingAsset.as_view(), name="missing_asset"),
    path("api/assign-asset-to-role/", AssignAssetToRole.as_view(), name="assign_asset_role"),
    path("api/entity-exists/", EntityExist.as_view(), name="entity_exists"),
    path("api/retire-asset/", RetireAsset.as_view(), name="retire_asset"),
    path("api/dev-explore/", DevExplorationView.as_view(), name="dev_explore"),
    path("api/set-role-parent/", RoleParent.as_view(), name="set_role_parent"),
]