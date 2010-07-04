from piston.handler import BaseHandler
from step2.project.models import Project, Task
from step2.forum.models import Forum, Thread

class ProjectsHandler(BaseHandler):
    model = Project
    fields = ('id', 'name')

    def read(self, request):
        projects = Project.objects
        return projects.all()


class ProjectHandler(BaseHandler):
    model = Project
    fields = ('id', 'name', 'description', 'state', 'created_date', 'tags',
              ('members', ('id', 'username', 'first_name', 'last_name')),
              ('forum', ('id', 'title')))

    def read(self, request, id):
        try:
            project = Project.objects.get(pk=id)
            return project
        except Project.DoesNotExist:
            return {}


class AllTasksHandler(BaseHandler):
    model = Task
    fields = ('id', 'title', 'description')

    def read(self, request):
        tasks = Task.objects
        return tasks.all()


class ProjectTasksHandler(BaseHandler):
    model = Task
    fields = ('id', 'title', 'description')

    def read(self, request, id):
        tasks = Task.objects.filter(belongs_to_project=id)
        return tasks.all()


class TaskHandler(BaseHandler):
    model = Task
    fields = ('id', 'title', 'created_date', 'due_date', 'state', 'completed_date', 'description', 'priority',
              ('created_by', ('id', 'username', 'first_name', 'last_name')),
              ('assigned_to', ('id', 'username', 'first_name', 'last_name')),
              ('belongs_to_project', ('id', 'name')))

    def read(self, request, id):
        try:
            task = Task.objects.get(pk=id)
            return task
        except Task.DoesNotExist:
            return {}


class ForumsHandler(BaseHandler):
    model = Forum
    fields = ('id', 'title')

    def read(self, request):
        forums = Forum.objects
        return forums.all()


class ForumHandler(BaseHandler):
    model = Forum
    fields = ('id', 'title', 'slug', 'parent', 'description', 'threads', 'posts',
              ('groups', ('name')))

    def read(self, request, id):
        try:
            forum = Forum.objects.get(pk=id)
            return forum
        except Forum.DoesNotExist:
            return {}
