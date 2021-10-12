from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from ghtc.domain.commit import ConventionalCommitMessage


class Override(BaseModel):

    hexsha: str
    commit: ConventionalCommitMessage


class OverrideBackendInterface(ABC):
    @abstractmethod
    def get_override(self, hexsha: str) -> Optional[ConventionalCommitMessage]:
        raise NotImplementedError()


class OverrideController:
    def __init__(self, backend: OverrideBackendInterface):
        self.backend: OverrideBackendInterface = backend

    def get_override(self, hexsha: str) -> Optional[ConventionalCommitMessage]:
        return self.backend.get_override(hexsha)
