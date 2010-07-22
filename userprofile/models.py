from django.db import models
from django.contrib.auth.models import User
from south.modelsinspector import add_introspection_rules
from tagging.fields import TagField

add_introspection_rules = ([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

class SkillSet(models.Model):
    skill = models.CharField(max_length=100)
    description = models.TextField(max_length=500)


class UserProfile(models.Model):
    choices = (('S', 'Student'),
               ('I', 'Professional'))

    role    = models.CharField(max_length=1, choices=choices, default='I')
    profile = models.TextField(max_length=500)
    aoi     = TagField(blank=True, null=True)
    user    = models.ForeignKey(User, unique=True)
    skills  = models.ManyToManyField(SkillSet, blank=True, null=True)


