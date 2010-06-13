from django.db import models
from django.contrib.auth.models import User
from south.modelsinspector import add_introspection_rules
from tagging.fields import TagField
from step2.forum.models import Forum


add_introspection_rules = ([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

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
    created_by = models.ForeignKey(User, related_name='projects_created')
    tags = TagField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self):
        if not self.id:
            self.created_date = datetime.datetime.now()

        super(Item, self).save()
