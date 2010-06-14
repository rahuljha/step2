from django.contrib import admin
from step2.project.models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
        ]

admin.site.register(Project, ProjectAdmin)

