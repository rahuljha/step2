from django.db import models
from django.contrib.auth.models import User
from step2.project.models import Project

# Create your models here.
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

    # Auto-set the task creation / completed date
    def save(self):
        # Set datetime on initial item save
        if not self.id:
            self.created_date = datetime.datetime.now()

        # If task is being marked complete, set the completed_date
        if self.completed :
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]
