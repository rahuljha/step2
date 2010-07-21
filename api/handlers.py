from piston.handler import BaseHandler
from piston.utils import rc, throttle #TODO: use throttle

from django.contrib.auth.models import User
from step2.project.models import Project, Task
from step2.forum.models import Forum, Thread, Post

def create_response(response, mesg):
    response.write(" " + str(mesg))
    return response

class ProjectsHandler(BaseHandler):
    allowed_methods = ('GET', 'POST',)
    model = Project
    fields = ('id', 'name')

    def read(self, request):
        return Project.objects.all()

    def create(self, request):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN

        if request.content_type:
            data = request.data

            forum = Forum(title="A forum for project " + data['name'],
                          description="a forum for discussions on the project " + data['name'])
            forum.save()

            owner = None
            if not 'owner_id' in data:
                owner = request.user
            else:
                owner = User.objects.get(pk=data['owner_id'])

            project = self.model(name=data['name'],
                                 owner=owner,
                                 created_by=request.user,
                                 description=data['description'],
                                 forum=forum)
            project.save()

            for member in data['members']:
                user = User.objects.get(pk=member['id'])
                project.members.add(user)

                return (rc.CREATED, project.id);
        # else:
        # TODO: the data is not a json string, maybe a dataform?, need to handle this


class ProjectHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Project
    fields = ('id', 'name', 'owner', 'created_by', 'description', 'state', 'created_date', 'tags',
              ('members', ('id', 'username', 'first_name', 'last_name')),
              ('forum', ('id', 'title')))

    def __update(self, project, data):
        if 'name' in data: project.name = data['name']
        if 'description' in data: project.description = data['description']
        if 'owner_id' in data: project.owner = User.objects.get(pk=data['owner_id'])
        if 'state' in data: project.state = data['state']

        if 'members' in data:
            for member in data['members']:
                user = User.objects.get(pk=member['id'])
                project.members.add(user)   #adding a user which is already present should be OK

        return project

    def read(self, request, id):
        try:
            project = Project.objects.get(pk=id)
            return project
        except Project.DoesNotExist:
            return {}

    def update(self, request, id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN

        if request.content_type:
            data = request.data

            try:
                project = Project.objects.get(pk=id)
            except Project.DoesNotExist:
                return create_response(rc.NOT_HERE,'project with id ' + id + ' does not exist')

            if request.user == project.owner or [member for member in project.members.all() if request.user == member]:
                self.__update(project, data).save()
                return rc.ALL_OK
            else:
                return create_response(rc.FORBIDDEN,
                                       request.user.username + ' is not the owner or one of the members of the project')

    def delete(self, request, id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN

        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExist:
            return create_response(rc.NOT_HERE,'project with id ' + id + ' does not exist')

        if project.owner == request.user:
            project.delete()
            return rc.DELETED
        else:
            return create_response(rc.FORBIDDEN, request.user.username + ' is not the owner of the project')


class AllTasksHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET', 'POST',)
    fields = ('id', 'title', 'description')

    def read(self, request):
        tasks = Task.objects
        return tasks.all()

    def create(self, request):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN

        if request.content_type:
            data = request.data

            assigned_to = request.user  # optional fields
            if 'assigned_to' in data:
                assigned_to = User.objects.get(pk=data['assigned_to'])

            due_date = None             # optional field
            if 'due_date' in data:
                due_date = data['due_date']

            task = self.model(title=data['title'],
                              due_date=due_date,
                              created_by=request.user,
                              assigned_to=assigned_to,
                              belongs_to_project=Project.objects.get(pk=data['belongs_to_project']),
                              description=data['description'],)

            task.save()
            return create_response(rc.CREATED, task.id)


class ProjectTasksHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET',)
    fields = ('id', 'title', 'description', 'created_date', 'due_date',
              ('assigned_to', ('id', 'username')),
              'state')

    def read(self, request, id):
        return Task.objects.filter(belongs_to_project=id)


class TaskHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET', 'DELETE', 'PUT',)
    fields = ('id', 'title', 'created_date', 'due_date', 'state', 'completed_date', 'description',
              ('created_by', ('id', 'username', 'first_name', 'last_name')),
              ('assigned_to', ('id', 'username', 'first_name', 'last_name')),
              ('belongs_to_project', ('id', 'name')))

    def __update(self, task, data):
        if 'title' in data: task.name = data['title']
        if 'description' in data: task.description = data['description']
        if 'state' in data: task.state = data['state']
        if 'due_date' in data: task.due_date = data['due_date']
        if 'assigned_to_id' in data: task.assigned_to = User.objects.get(pk=data['assigned_to_id'])
        return task

    def read(self, request, id):
        try:
            task = Task.objects.get(pk=id)
            return task
        except Task.DoesNotExist:
            return {}

    def update(self, request, id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN
        if request.content_type:
            data = request.data
            try:
                task = Task.objects.get(pk=id)
            except Task.DoesNotExist:
                return create_response(rc.NOT_HERE, 'task with id ' + id + ' does not exist')
            self.__update(task, data).save()
            return rc.ALL_OK

    def delete(self, request, id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN
        try:
            task = Task.objects.get(pk=id)
        except Task.DoesNotExist:
            return create_response(rc.NOT_HERE, 'task with id ' + id + ' does not exist')
        if task.created_by == request.user:
            task.delete()
            return rc.DELETED
        else:
            return create_response(rc.FORBIDDEN, request.user.username + ' is not allowed to delete a task')


class ForumsHandler(BaseHandler):
    model = Forum
    fields = ('id', 'title')

    def read(self, request):
        return Forum.objects.all()

class ForumHandler(BaseHandler):
    model = Forum
    fields = ('id', 'title', 'slug', 'parent', 'description', 'threads', 'posts',
              ('groups', ('name')))

    def read(self, request, project_id=None, forum_id=None):
        if project_id:
            try:
                return Project.objects.get(pk=project_id).forum
            except Project.DoesNotExist:
                {}
        elif forum_id:
            try:
                return Forum.objects.get(pk=forum_id)
            except Forum.DoesNotExist:
                return {}
        else:
            return rc.BAD_REQUEST


class ForumThreadsHandler(BaseHandler):
    model = Thread
    allowed_methods = ('GET', 'POST',)
    fields = ('id', 'title', 'closed', 'posts', 'views',)

    def read(self, request, id):
        return Thread.objects.filter(forum=id)


class ThreadPostsHandler(BaseHandler):
    model = Post
    allowed_methods = ('GET', 'POSt',)
    fields = ('id', 'time', 'body_html', ('author', ('id', 'username')),)

    def read(self, request, id):
        return Post.objects.filter(thread=id)
