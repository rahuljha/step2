from django.db import models
from django.contrib.auth.models import User
from south.modelsinspector import add_introspection_rules 

class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    member = models.ManyToManyField(User)
    forum = models.ForeignKey('forum.Forum', unique=True)
    state = models.CharField(max_length=1, choices=(('I', 'Incubation'),
                                                    ('L', 'Looking for Resources'),
                                                    ('W', 'In Progress'),
                                                    ('M', 'Maintainence'),
                                                    ), 
                             default='I')
    posted_on = models.DateField(null=True)

    def __unicode__(self):
        return self.name
