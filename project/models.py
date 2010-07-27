import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import admin
from south.modelsinspector import add_introspection_rules
from tagging.fields import TagField
from forum.models import Forum
from userprofile.models import SkillSet
from django.template.defaultfilters import slugify

add_introspection_rules = ([], ["tagging_autocomplete\.models\.TagAutocompleteField"])


class Project(models.Model):
    project_state_choices = (('I', 'Incubation'),
                             ('L', 'Looking for Resources'),
                             ('W', 'In Progress'),
                             ('M', 'Maintainence'))

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, related_name='projects_owner')
    created_by = models.ForeignKey(User, related_name='projects_created')
    members = models.ManyToManyField(User)
    forum = models.ForeignKey(Forum, unique=True, null=True, blank=True)
    state = models.CharField(max_length=1, choices=project_state_choices, default='I')
    created_date = models.DateField(auto_now_add=True)
    required_skills = models.ManyToManyField(SkillSet, blank=True, null=True)
    tags = TagField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True);

    def __unicode__(self):
        return self.name

    def save(self):
        forum = Forum(title="A forum for project " + self.name,
                      description="a little nudge from us to get you all up and running...")
        forum.save()
        self.forum = forum
        self.slug = slugify(self.name);
        super(Project, self).save()


class Task(models.Model):
    task_state_choices = (('O', 'open'),
                          ('C', 'closed'))

    title = models.CharField(max_length=140)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True,null=True,)
    state = models.CharField(max_length=1, choices=task_state_choices, default='O')
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned')
    belongs_to_project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    def overdue_status(self):
        "Returns whether the task's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title

    def save():
        self.slug = slugify(self.title);
        super(Task, self).save()

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class TaskForm(ModelForm):
    class Meta:
        model = Task
