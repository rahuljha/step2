from piston.handler import BaseHandler
from piston.utils import rc, throttle #TODO: use throttle

from django.contrib.auth.models import User
from step2.project.models import Project, Task
from step2.forum.models import Forum, Thread

def create_response(response, mesg):
    response.write(mesg)
    return response

class ProjectsHandler(BaseHandler):
    allowed_methods = ('GET', 'POST',)
    model = Project
    fields = ('id', 'name')

    def read(self, request):
        projects = Project.objects
        return projects.all()

    def create(self, request):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN

        if request.content_type:
            data = request.data

            forum = None
            if 'forum_id' in data:
                forum=Forum.objects.get(pk=data['forum_id'])
            elif 'forum' in data:
                forum = None #TODO create from json string
            else:
                return create_response(rc.BAD_REQUEST,
                                       ' either provide a forum id or a forum json string in the request data')

            owner = None
            if not 'owner_id' in data:
                owner = request.user
            else:
                owner = User.objects.get(pk=data['owner_id'])

            project = self.model(name=data['name'], owner=owner, created_by=request.user, description=data['description'], forum=forum)
            project.save()

            for member in data['members']:
                user = User.objects.get(pk=member['id'])
                project.members.add(user)

                return rc.CREATED
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
        if 'description' in data: project.name = data['description']
        if 'owner' in data: project.name = data['owner']
        if 'state' in data: project.name = data['state']

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
                return create_response(rc.NOT_HERE,
                                       'project with id ' + id + ' does not exist')

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
            return create_response(rc.NOT_HERE, ' project with id ' + id + ' does not exist')

        if project.owner == request.user:
            project.delete()
            return rc.DELETED
        else:
            return create_response(rc.FORBIDDEN, request.user.username + ' is not the owner of the project')


class AllTasksHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET',)
    fields = ('id', 'title', 'description')

    def read(self, request):
        tasks = Task.objects
        return tasks.all()


class ProjectTasksHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET',)
    fields = ('id', 'title', 'description')

    def read(self, request, id):
        tasks = Task.objects.filter(belongs_to_project=id)
        return tasks.all()


class TaskHandler(BaseHandler):
    model = Task
    allowed_methods = ('GET', 'DELETE', 'PUT', 'POST')
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

    #def create(self, request):
    #    data = request.POST
        # createProject(data)

    # def update(self, request, id):
    #     task = Task.objects.get(pk=id)

    #     if not task.owner == request.user:
    #         return rc.FORBIDDEN

    #     updatedTask = updateTask(task, request.POST)
    #     return updateTask

    # def delete(self, request, id):
    #     task = Task.objects.get(pk=id)

    #     if not task.owner == request.user:
    #         return rc.FORBIDDEN

    #     task.delete()
    #     return rc.DELETED



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

    # def update(self, request, id):
    #     forum = Forum.objects.get(pk=id)

    #     if not forum.owner == request.user:
    #         return rc.FORBIDDEN

    #     updatedForum = updateForum(forum, request.POST)
    #     return updateForum

    # def delete(self, request, id):
    #     forum = Forum.objects.get(pk=id)

    #     if not forum.owner == request.user:
    #         return rc.FORBIDDEN

    #     forum.delete()
    #     return rc.DELETED

