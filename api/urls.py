from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
#from piston.doc import documentation_view

from step2.api.handlers import *

auth = HttpBasicAuthentication(realm='step2 api')

project = Resource(handler=ProjectHandler, authentication=auth)
projects = Resource(handler=ProjectsHandler, authentication=auth)

task = Resource(handler=TaskHandler, authentication=auth)
all_tasks = Resource(handler=AllTasksHandler, authentication=auth)
project_tasks = Resource(handler=ProjectTasksHandler, authentication=auth)

forum = Resource(handler=ForumHandler, authentication=auth)
forums = Resource(handler=ForumsHandler, authentication=auth)

urlpatterns = patterns('',
                       url(r'^projects/$', projects),
                       url(r'^projects/(\d+)$', project),

                       url(r'^projects/tasks/$', all_tasks),   # is this required?
                       url(r'^projects/(\d+)/tasks/$', project_tasks),

                       url(r'^projects/tasks/(\d+)/$', task),

                       url(r'^forums/$', forums),
                       url(r'^forums/(\d+)/$', forum),

                       # to be added, if required
                       # url(r'^forums/(\d+)/threads/$', forum_threads),
                       # url(r'^forums/threads/(\d+)/$', thread),

                       # url(r'^forums/threads/(\d+)/posts/$', thread_posts),
                       # url(r'^forums/threads/posts/(\d+)/$', post),
                       )

