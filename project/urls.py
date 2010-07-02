from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update

from project.models import Project, Task
from project.views import list_tasks, edit_task

project_list_info = {
    'queryset': Project.objects.all(),
    'template_name': "project/project_list.html",
    'template_object_name': "projects",
}

project_detail_info = {
    'queryset': Project.objects.all(),
    'template_name': "project/project_detail.html",
    'template_object_name' : "project",
}

project_edit_info = {
    'model': Project,
    'template_name': "project/project_edit.html",
    'post_save_redirect': "projects/",
    'template_object_name' : "project",
}

task_list_info = {
    'queryset': Task.objects.all(),
    'template_name': "task/task_list.html",
    'template_object_name' : "tasks",
}

task_detail_info = {
    'queryset': Task.objects.all(),
    'template_name': "task/task_detail.html",
    'template_object_name' : "task",
}

task_edit_info = {
    'model': Task,
    'template_name': "task/task_edit.html",
    'post_save_redirect': "tasks/",
    'template_object_name' : "task",
}

task_create_info = {
    'model': Task,
    'post_save_redirect': "tasks/",
    'template_name': "task/task_create.html",
}

urlpatterns = patterns('',
                       (r'^$', list_detail.object_list, project_list_info),
                       (r'^(?P<object_id>\d+)/$', list_detail.object_detail, project_detail_info),
                       (r'^(?P<object_id>\d+)/edit/$', create_update.update_object, project_edit_info),
                       (r'^tasks/$', list_detail.object_list, task_list_info), # a paginated view of all the tasks
                       (r'^(\d+)/tasks/$', list_tasks), # tasks belonging to a particular project
                       (r'^tasks/(\d+)/edit/$', edit_task),
                       (r'^tasks/(?P<object_id>\d+)/$', list_detail.object_detail, task_detail_info),
                       (r'^tasks/create/$', create_update.create_object, task_create_info))


