from django.http import HttpResponse #temporary
from django.views.generic import list_detail
from project.models import Project, Task

from django.views.generic import create_update
from project.permissions import ProjectPermission
from django.contrib.auth.models import User

############signals#################
from django.db.models.signals import post_save
#from project.models import


def list_tasks(request, project_id):
    return list_detail.object_list(
        request,
        queryset = Task.objects.filter(belongs_to_project=project_id),
        template_name = "task/task_list.html",
        template_object_name = "tasks")

def edit_task(request, project_id):
    return HttpResponse("temporary")

################signals####################
def project_signalhandler(sender,instance,**kwargs):
        owner = instance.owner#instance of the object
        check = ProjectPermission(owner)
        check.assign(None,instance)
        """None makes sure that all the permissions are assigned
        if a specific permission is needed to be assigned pass it as a string instead of None
        eg: check.assign('edit_project',instance)"""


post_save.connect(project_signalhandler, sender=Project)
