"""
This module contains the data models for the import_from_modulestore app.
"""
from __future__ import annotations

from enum import Enum

from openedx.core.djangoapps.content_libraries.api import ContainerType


class CompositionLevel(Enum):
    """
    Enumeration of composition levels for legacy content.
    """
    # These are defined in increasing order of complexity so that `is_higher_than` works correctly.
    Component = 'component'
    Unit = ContainerType.Unit.value
    Subsection = ContainerType.Subsection.value
    Section = ContainerType.Section.value
    OutlineRoot = 'outline_root'  # The list of sections that make up the course outline
    CourseRun = 'course_run'  # The OutlineRoot plus all other associated course items (about page, custom tabs, etc)

    @property
    def is_container(self) -> bool:
        return self is not self.Component

    def is_higher_than(self, other: 'CompositionLevel') -> bool:
        """
        Is this composition level 'above' (more complex than) the other?
        """
        levels: list[CompositionLevel] = list(self.__class__)
        return levels.index(self) > levels.index(other)

    @classmethod
    def supported_choices(cls) -> list[tuple[str, str]]:
        """
        Returns all supported composition levels as a list of tuples,
        for use in a Django Models ChoiceField.
        """
        return [
            (composition_level.value, composition_level.name)
            for composition_level in cls
            # Currently, we do not support import nodes any higher than the Section.
            if not composition_level.is_higher_than(cls.Section)
        ]
