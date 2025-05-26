"""
This module contains the data models for the import_from_modulestore app.
"""
from collections import namedtuple
from enum import Enum

from openedx.core.djangoapps.content_libraries.api import ContainerType

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
        WAITNG_TO_STAGE: _('Waiting to stage content'),
        STAGING: _('Staging content for import'),
        STAGED: _('Content is staged and ready for import'),
        IMPORTING: _('Importing staged content'),
    }


class CompositionLevel(Enum):
    """
    Enumeration of composition levels for course content, increasing order of complexity.

    Defines the different levels of composition for course content, including chapters, sequentials, verticals, and xblocks.
    """

    Component = 'component'
    Unit = ContainerType.Unit.value
    Subsection = ContainerType.Subsection.value
    Section = ContainerType.Section.value

    @property
    def is_complex(self):
        return self is not self.Component

    '''
    @property
    def is_supported(self):
        """
        Do we allow imports at this composition level?

        Note on OutlineRoot:
            The XML tags <course> and <library_root> represent the roots of legacy courses and legacy content
            libraries, respectively. In the future, we may support importing these into learning packages as
            aggregated "OutlineRoot" containers. However, we are still in the process of considering and designing
            the OutlineRoot container, so rather than support this operation now, we raise ane exception
            if someone tries to import and entire aggregated legacy course or legacy library.
        """
        return self is not self.OutlineRoot

    @classmethod
    def from_source_olx_tag(cls, olx_tag: str) -> 'CompositionLevel':
        """
        Get the CompositionLevel that this OLX tag maps to.

        All OLX tags which are not recognized as Containers or roots are assumed to be Components.
        """
        if olx_tag == 'course' or olx_tag == 'library_root':
            raise NotImplementedError("Importing root tag <{olx_tag}> is not yet supported. Import its children instead.")
        try:
            return CompositionLevel(ContainerType.from_source_olx_tag(olx_tag).value)
        except ValueError:
            return CompositionLevel.Component
    '''

    @classmethod
    def values(cls):
        """
        Returns all levels of composition levels.
        """
        return [composition_level.value for composition_level in cls]

    @classmethod
    def choices(cls):
        """
        Returns all supported levels of composition levels as a list of tuples.
        """
        return [
            (composition_level.value, composition_level.name)
            for composition_level in cls
        ]


PublishableVersionWithMapping = namedtuple('PublishableVersionWithMapping', ['publishable_version', 'mapping'])