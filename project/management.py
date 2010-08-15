from django.conf import settings
from django.utils.translation import ugettext_noop as _noop
from django.db.models.signals import post_syncdb

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("task_created", "Task Created", "A new task was created")
    
    post_syncdb.connect(create_notice_types, sender=notification)

else:
    print "Skipping creation of NoticeTypes as notification app not found"
