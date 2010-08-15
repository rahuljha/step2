import authority
from authority import permissions
from project.models import Project

class ProjectPermission(permissions.BasePermission):
    label = 'project_permission' # use small case for label else it causes trouble in internal authority code
    checks = ('review','edit')

authority.register(Project, ProjectPermission)
