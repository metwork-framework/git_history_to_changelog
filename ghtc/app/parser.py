from abc import ABC, abstractmethod
from typing import List, Optional

from ghtc.domain.changelog import ChangelogEntry


class ParserBackendInterface(ABC):
    @abstractmethod
    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        raise NotImplementedError()

    @abstractmethod
    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        raise NotImplementedError


class ParserController:
    def __init__(self, parsers: List[ParserBackendInterface]):
        self.parsers: List[ParserBackendInterface] = parsers

    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        for p in self.parsers:
            cle: List[ChangelogEntry] = p.parse(commit_message)
            if len(cle) > 0:
                return cle
        return []

    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        for p in self.parsers:
            sha: Optional[str] = p.get_reverted_commit(commit_message)
            if sha is not None:
                return sha
        return None
