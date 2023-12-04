from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class LibraryVersionQuery(ABC):
    """
    """

    def build_blockstore_definition_key(self, bundle_uuid: UUID, olx_path: str, latest_version_number: int) -> BundleDefinitionLocator:
        raise NotImplementedError



@dataclass(frozen=True)
class LastPublished(LibraryVersionQuery):
    """
    """
    def build_blockstore_definition_key(self, bundle_uuid, olx_path):
        return BundleDefinitionLocator(bundle_uuid=bundle_uuid, olx_path=olx_path,


@dataclass(frozen=True)
class SpecificVersion(LibraryVersionQuery):
    """
    """
    version_number: int


@dataclass(frozen=True)
class Draft(LibraryVersionQuery):
    """
    """

