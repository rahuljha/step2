from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update

from project.models import Project

project_list_info = {
    'queryset': Project.objects.all(),
    'template_name': "project/project_list.html",
    'template_object_name' : "project_list",
}

project_detail_info = {
    'queryset': Project.objects.all(),
    'template_name': "project/project_detail.html",
    'template_object_name' : "project",
}

project_edit_info = {
    'model': Project,
    'template_name': "project/project_edit.html",
    'post_save_redirect': "project/",
    'template_object_name' : "project",
}


urlpatterns = patterns('',
                       (r'^$', list_detail.object_list, project_list_info),
                       (r'^view/(?P<object_id>\d+)/$', list_detail.object_detail, project_detail_info),
                       (r'^edit/(?P<object_id>\d+)/$', create_update.update_object, project_edit_info),
                       (r'^tasks/$', list_detail.object_list, task_list_info),
                       (r'^/task/view/(?P<object_id>\d+)/$', list_detail.object_detail, task_detail_info),
                       (r'^/task/edit/(?P<object_id>\d+)/$', list_detail.update_object, task_edit_info),
                       )
