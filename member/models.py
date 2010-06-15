from django.db import models
from django.contrib.auth.models import User
from south.modelsinspector import add_introspection_rules
from tagging.fields import TagField

add_introspection_rules = ([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

class Member(models.Model):
    Role    = models.CharField(max_length=1,
                            choices = (('S', 'Student'),
                                       ('I', 'Professionals'),),
                            default='I')
    Profile = models.TextField(max_length=500)
    AOI     = models.TextField(max_length=300)
    user    = models.ForeignKey(User, unique=True)  ## each member is an unique user

