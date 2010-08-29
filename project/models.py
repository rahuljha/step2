from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.http import HttpRequest
from django.template.defaultfilters import slugify
from forum.models import Forum
from notification import models as notification
from south.modelsinspector import add_introspection_rules
from tagging.fields import TagField
from userprofile.models import SkillSet

import datetime

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
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        forum = Forum(title="A forum for project " + self.name,
                       description="Use this as a starting point for various discussions and Q&A")
        forum.save()
        self.forum = forum
        self.slug = slugify(self.name);
        super(Project, self).save()

def project_onsave(sender, instance, created, **kwargs):
    if created==True:
        notification.send([instance.owner], 'project_created',{'project_obj': instance})
    else:
        notification.send([instance.owner], 'project_updated',{'project_obj': instance, 'updater': HttpRequest.user})

### register signals
post_save.connect(project_onsave, sender=Project)


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
    slug = models.SlugField(blank=True, null=True)

    def overdue_status(self):
        "Returns whether the task's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title);
        super(Task, self).save()


def task_onsave(sender, instance, created, **kwargs):
    if created==True:
        notification.send([instance.assigned_to, instance.created_by], 'task_created',{'task_obj': instance})
    else:
        notification.send([instance.assigned_to, instance.created_by], 'task_updated',{'task_obj': instance, 'updater': HttpRequest.user})

### register signal
post_save.connect(task_onsave, sender=Task)
