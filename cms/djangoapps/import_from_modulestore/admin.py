"""
This module contains the admin configuration for the Import model.
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Import, PublishableEntityImport, PublishableEntityMapping


class ImportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Import model.
    """

    list_display = (
        'source_key',
        'composition_level',
        'update_existing',
        'target',
        'target_collection',
        'target_change',
        'task_status',
        'task_state',
        'task_started_by',
    )
    search_fields = ('source_key', 'target', 'target_collection')
    readonly_fields = ('task_status', 'target_change')

    def task_status(self, obj: Import) -> str:
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:user_tasks_usertaskstatus_change", args=(obj.task_status.pk,)),
            f"{obj.task_status.uuid}",
        )) if obj.task_status else "(Task not yet created)"

    def task_state(self, obj: Import) -> str:
        return obj.task_status.state if obj.task_status else None

    def task_started_by(self, obj: Import):
        return obj.task_status.user if obj.task_status else None

admin.site.register(Import, ImportAdmin)
admin.site.register(PublishableEntityImport)
admin.site.register(PublishableEntityMapping)
