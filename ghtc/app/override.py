from abc import ABC, abstractmethod
from typing import List

from ghtc.domain.changelog import ChangelogEntry


class OverrideBackendInterface(ABC):
    @abstractmethod
    def get_override(self, hexsha: str) -> List[ChangelogEntry]:
        raise NotImplementedError()


class OverrideController:
    def __init__(self, backend: OverrideBackendInterface):
        self.backend: OverrideBackendInterface = backend

    def get_override(self, hexsha: str) -> List[ChangelogEntry]:
        return self.backend.get_override(hexsha)
