from django.http import HttpResponse #temporary
from django.views.generic import list_detail
from project.models import Task

def list_tasks(request, project_id):
    return list_detail.object_list(
        request,
        queryset = Task.objects.filter(belongs_to_project=project_id),
        template_name = "task/task_list.html",
        template_object_name = "tasks")

def edit_task(request, project_id):
    return HttpResponse("temporary")
