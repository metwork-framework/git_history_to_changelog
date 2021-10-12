import re
from abc import ABC, abstractmethod
from typing import List

from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, Tag


class RepoBackendInterface(ABC):
    @abstractmethod
    def get_tags(self) -> List[Tag]:
        raise NotImplementedError()

    @abstractmethod
    def get_first_commit(self) -> Commit:
        raise NotImplementedError()

    @abstractmethod
    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        raise NotImplementedError()


class RepoController:
    def __init__(self, backend: RepoBackendInterface):
        self.backend: RepoBackendInterface = backend

    def get_tags(self, tags_regex: str = ".*") -> List[Tag]:
        compiled_pattern = re.compile(tags_regex)
        res = []
        for tag in self.backend.get_tags():
            if re.match(compiled_pattern, tag.name):
                res.append(tag)
        return sorted(res, key=lambda x: x.tagged_date)

    def get_first_commit(self) -> Commit:
        return self.backend.get_first_commit()

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        return self.backend.get_commits_between(tag1, tag2)

    def get_commits(self) -> List[Commit]:
        return self.get_commits_between(BeginningTag(), HeadTag())
