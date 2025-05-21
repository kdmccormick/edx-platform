"""
This module contains the data models for the import_from_modulestore app.
"""
from collections import namedtuple
from enum import Enum

from openedx.core.djangoapps.content_libraries import api as content_libraries_api

from django.utils.translation import gettext_lazy as _


class ImportProgressState:
    """
    Strings representation the state of an in-progress modulestore-to-learning-core import.

    The full set of Import states is the union of these and UserTaskStatus.{PENDING,FAILED,CANCELED,SUCCEEDED}.
    """
    WAITNG_TO_STAGE = 'Waiting to stage content'
    STAGING = 'Staging content for import'
    STAGED = 'Content is staged and ready for import'
    IMPORTING = 'Importing staged content'

    STATE_TRANSLATIONS = {
        WAITNG_TO_STAGE = _('Waiting to stage content'),
        STAGING = _('Staging content for import'),
        STAGED = _('Content is staged and ready for import'),
        IMPORTING = _('Importing staged content'),
    }


class CompositionLevel(Enum):
    """
    Enumeration of composition levels for course content, increasing order of complexity.

    Defines the different levels of composition for course content, including chapters, sequentials, verticals, and xblocks.
    """

    Component = 'component'
    Unit = content_libraries_api.ContainerType.Unit
    Subsection = content_libraries_api.ContainerType.Subsection
    Section = content_libraries_api.ContainerType.Section

    @property
    def is_complex(self):
        return self is not self.Component

    @classmethod
    def values(cls):
        """
        Returns all levels of composition levels.
        """
        return [composition_level.value for composition_level in cls]

    @classmethod
    def choices(cls):
        """
        Returns all levels of composition levels as a list of tuples.
        """
        return [
            (composition_level.value, composition_level.name)
            for composition_level in cls
        ]


@dataclasss
class ImportData:
    

