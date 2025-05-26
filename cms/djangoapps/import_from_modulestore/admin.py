"""
This module contains the admin configuration for the Import model.
"""
from __future__ import annotations

from django.db.models import QuerySet
from django.contrib import admin, messages
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Import, PublishableEntityImport, PublishableEntityMapping
from .api import start_import_from_modulestore_task


@admin.action(description="Start new import task")
def start_new_import_task(modeladmin: ImportAdmin, request, queryset: QuerySet[Import]):
    """
    todo
    """
    if not queryset:
        modeladmin.message_user(request, "No Import objects selected to start", level=messages.WARNING)
        return
    num_started = len(queryset)
    for import_model in queryset:
        start_import_from_modulestore_task(request.user, import_model)
    modeladmin.message_user(request, f"Started {num_started} import tasks", level=messages.SUCCESS)


class ImportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Import model.
    """

    list_display = (
        'source_key',
        'composition_level',
        'replace_existing',
        'target',
        'target_collection',
        'target_change',
        'task_status',
        'task_state',
        'task_started_by',
    )
    search_fields = ('source_key', 'target', 'target_collection')
    readonly_fields = ('task_status', 'target_change')
    actions = [start_new_import_task]

    def task_status(self, obj: Import) -> str:
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:user_tasks_usertaskstatus_change", args=(obj.task_status.pk,)),
            f"{obj.task_status.uuid}",
        )) if obj.task_status else "(Task not yet created)"

    def task_state(self, obj: Import) -> str:
        return obj.task_status.state if obj.task_status else None

    def task_started_by(self, obj: Import) -> AbstractUser:
        return obj.task_status.user if obj.task_status else None


admin.site.register(Import, ImportAdmin)
admin.site.register(PublishableEntityImport)
admin.site.register(PublishableEntityMapping)
