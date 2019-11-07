from dataclasses import dataclass, field


@dataclass(order=True)
class DisplayUserProjects:
    """Simple Class for displaying which projects a user belongs to"""
    project_number: str
    project_name: str
    user_role: str
