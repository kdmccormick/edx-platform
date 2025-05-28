"""
Models for the course to library import app.
"""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from user_tasks.models import UserTaskStatus

from model_utils.models import TimeStampedModel
from opaque_keys.edx.django.models import (
    LearningContextKeyField,
    UsageKeyField,
)
from openedx_learning.api.authoring_models import (
    LearningPackage, PublishableEntity, Collection, DraftChangeLog, DraftChangeLogRecord
)

from openedx.core.djangoapps.content_staging.models import StagedContent
from .data import CompositionLevel

User = get_user_model()


class Import(models.Model):
    """
    The action of a user importing a ModuleStore-based course or legacy library into a
    learning-core based learning package

    (Note: Currently, a learning package is always a content library.)

    Each Import is tied to a single UserTaskStatus, which connects the Import to a user and
    tracks the progress of the import.
    """
    task_status = models.OneToOneField(
        UserTaskStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modulestore_import',
    )
    source_key = LearningContextKeyField(
        max_length=255,
        db_index=True,
        help_text=_('Key of the content source (a course or a legacy library)')
    )
    composition_level = models.CharField(
        max_length=255,
        choices=CompositionLevel.choices(),
        help_text=_('Maximum hierachy level at which content should be aggregated in target library'),
        default=CompositionLevel.Component.value,
    )
    replace_existing = models.BooleanField(
        default=False,
        help_text=_(
            'If a piece of content already exists in the content library, should the import process replace it?'
        ),
    )
    target = models.ForeignKey(
        LearningPackage,
        on_delete=models.CASCADE,
        help_text=_('Content will be imported into this library'),
    )
    target_collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_('Optional - Collection (within the target library) into which imported content will be grouped'),
    )
    target_change = models.ForeignKey(
        DraftChangeLog, on_delete=models.SET_NULL, null=True,
        help_text=_('Changelog entry related to this import event'),
    )

    class Meta:
        verbose_name = _('ModuleStore Import')
        verbose_name_plural = _('ModuleStore Imports')

    def __str__(self):
        return f'ModuleStore Import #{self.pk}: {self.source_key} → {self.target}'

    def __repr__(self):
        return f"import_from_modulestore.Import(pk={self.pk}, source_key='{self.source_key}', target='{self.target}')"

    #def fail(self, message: str):
    #    """
    #    Mark the import as failed, with a message.
    #    """
    #    if not self.task_status:
    #        raise ValueError( f"Cannot mark {self!r} as failed... it does not even have an associated UserTaskStatus!")
    #    self.task_status.fail(message)

    #def set_progress_state(self: Self, state: ImportProgressState):
    #    """
    #    Mark the import as in-progress with a particular state.
    #    """
    #    if not self.task_status:
    #        raise ValueError(
    #            f"Cannot set state of {self!r} to {state} because the import does not yet "
    #            "have an associated UserTaskStatus. "
    #        )
    #    user_task_status.set_state(state)
    #    user_task_status.save()
    #    if status in [ImportStatus.IMPORTED, ImportStatus.CANCELED]:
    #        self.clean_related_staged_content()

    def clean_related_staged_content(self) -> None:
        """
        Clean related staged content.
        """
        for staged_content_for_import in self.staged_content_for_import.all():
            staged_content_for_import.staged_content.delete()


class PublishableEntityMapping(TimeStampedModel):
    """
    Represents a mapping between a source usage key and a target publishable entity.
    """
    source_usage_key = UsageKeyField(
        max_length=255,
        help_text=_('Original usage key of the XBlock that has been imported.'),
    )
    target_package = models.ForeignKey(LearningPackage, on_delete=models.CASCADE)
    target_entity = models.ForeignKey(PublishableEntity, on_delete=models.CASCADE)

    class Meta:
        # For any source legacy block, it can only be imported into a given learning package once.
        unique_together = ('source_usage_key', 'target_package')

    def __str__(self):
        return f'{self.source_usage_key} → {self.target_entity}'


class PublishableEntityImport(TimeStampedModel):
    """
    Represents a publishableentity version that has been imported into a learning package (e.g. content library)

    This is a many-to-many relationship between an entity version and a course to library import.
    """

    modulestore_import = models.ForeignKey(Import, on_delete=models.CASCADE)
    resulting_mapping = models.ForeignKey(PublishableEntityMapping, on_delete=models.SET_NULL, null=True, blank=True)
    resulting_change = models.OneToOneField(
        DraftChangeLogRecord,
        # a changelog record can be pruned, which would set this to NULL, but not delete the
        # entire import record
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = (
            ('modulestore_import', 'resulting_mapping'),
        )

    def __str__(self):
        return f'{self.modulestore_import} → {self.resulting_mapping}'


class StagedContentForImport(TimeStampedModel):
    """
    Represents m2m relationship between an import and staged content created for that import.
    """
    modulestore_import = models.ForeignKey(
        Import,
        on_delete=models.CASCADE,
        related_name='staged_content_for_import',
    )
    staged_content = models.OneToOneField(
        to=StagedContent,
        on_delete=models.CASCADE,
        related_name='staged_content_for_import',
    )
    # Since StagedContent stores all the keys of the saved blocks, this field was added to optimize search.
    source_usage_key = UsageKeyField(
        max_length=255,
        help_text=_(
            'The original Usage key of the highest-level component that was saved in StagedContent.'
        ),
    )

    class Meta:
        unique_together = (
            ('modulestore_import', 'staged_content'),
        )

    def __str__(self):
        return f'{self.modulestore_import} → {self.staged_content}'
