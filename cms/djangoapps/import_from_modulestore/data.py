"""
This module contains the data models for the import_from_modulestore app.
"""
from enum import Enum

from openedx.core.djangoapps.content_libraries.api import ContainerType

from django.utils.translation import gettext_lazy as _


class CompositionLevel(Enum):
    """
    Enumeration of composition levels for course content.
    """
    # These are defined in increasing order of complexity so that
    # `includes` works correctly.  If you add new composition levels,
    # be sure to keep the order correct. If you add compoisition levels
    # which do not fit into an obvious ordering, then adjust the implementation
    # of `includes` to handle that complexity.
    Component = 'component'
    Unit = ContainerType.Unit.value
    Subsection = ContainerType.Subsection.value
    Section = ContainerType.Section.value

    @property
    def is_complex(self):
        return self is not self.Component

    def is_higher_in_course_hierarchy(self, other: 'CompositionLevel') -> bool:
        """
        Is this composition level 'above' (more complex than the other?)
        """
        # mypy doesn't seem to understand that `self` is an instance of the enum.
        # self: 'CompositionLevel'
        levels: list[CompositionLevel] = list(self.__class__)
        return levels.index(self) > levels.index(other)

#  @@TODO
#    @property
#    def is_supported(self):
#        """
#        Do we allow imports at this composition level?
#
#        Note on OutlineRoot:
#            The XML tags <course> and <library_root> represent the roots of legacy courses and legacy content
#            libraries, respectively. In the future, we may support importing these into learning packages as
#            aggregated "OutlineRoot" containers. However, we are still in the process of considering and designing
#            the OutlineRoot container, so rather than support this operation now, we raise ane exception
#            if someone tries to import and entire aggregated legacy course or legacy library.
#        """
#        return self is not self.OutlineRoot
#
#    @classmethod
#    def from_source_olx_tag(cls, olx_tag: str) -> 'CompositionLevel':
#        """
#        Get the CompositionLevel that this OLX tag maps to.
#
#        All OLX tags which are not recognized as Containers or roots are assumed to be Components.
#        """
#        if olx_tag == 'course' or olx_tag == 'library_root':
#            raise NotImplementedError(
#                "Importing root tag <{olx_tag}> is not yet supported. Import its children instead."
#            )
#        try:
#            return CompositionLevel(ContainerType.from_source_olx_tag(olx_tag).value)
#        except ValueError:
#            return CompositionLevel.Component

    @classmethod
    def choices(cls):
        """
        Returns all supported levels of composition levels as a list of tuples,
        for use in a Django Models ChoiceField.
        """
        return [
            (composition_level.value, composition_level.name)
            for composition_level in cls
        ]
