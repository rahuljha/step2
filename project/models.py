import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from south.modelsinspector import add_introspection_rules

from tagging.fields import TagField
from forum.models import Forum

add_introspection_rules = ([], ["tagging_autocomplete\.models\.TagAutocompleteField"])

class Project(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    members = models.ManyToManyField(User)
    forum = models.ForeignKey(Forum, unique=True)
    state = models.CharField(max_length=1,
                             choices = (('I', 'Incubation'),
                                        ('L', 'Looking for Resources'),
                                        ('W', 'In Progress'),
                                        ('M', 'Maintainence'),),
                             default='I')
    created_date = models.DateField();
    tags = TagField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Task(models.Model):

    title = models.CharField(max_length=140)

    created_date = models.DateField()
    due_date = models.DateField(blank=True,null=True,)

    completed = models.BooleanField()
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned')
    belongs_to_project = models.ForeignKey(Project)
    members = models.ManyToManyField(User)
    description = models.TextField(blank=True)
    priority = models.PositiveIntegerField(max_length=3)

    def overdue_status(self):
        "Returns whether the task's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title


    class Meta:
        ordering = ["priority"]

