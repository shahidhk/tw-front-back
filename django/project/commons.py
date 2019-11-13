import datetime
from dataclasses import dataclass, field


@dataclass(order=True)
class DisplayUserProjects:
    """
    Simple Class for displaying which projects a user belongs to
    """
    project_number: str = ''
    project_name: str = ''
    user_role: str = ''
    project_type: str = ''


@dataclass(order=True)
class DisplayProjectDetails:
    """
    Class for Passing Project Detailed information to template
    """
    bus_unit: str = ''
    design_contract_number: str = ''
    project_manager: str = ''
    project_manager_email: str = ''
    key_bus_unit_contract: str = ''
    key_bus_unit_contract_email: str = ''
    asset_data_steward: str = ''
    asset_data_steward_email: str = ''
    project_scope_description: str = ''
    start_date: datetime.date = datetime.date.today()
