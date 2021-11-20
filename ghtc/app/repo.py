import re
from abc import ABC, abstractmethod
from typing import List, Optional

from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, SpecialTag, Tag


class RepoBackendInterface(ABC):
    @abstractmethod
    def get_all_tags(self) -> List[Tag]:
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
        res: List[Tag] = []
        compiled_pattern = re.compile(tags_regex)
        for tag in self.backend.get_all_tags():
            if re.match(compiled_pattern, tag.name):
                res.append(tag)
        return sorted(res, key=lambda x: x.date)

    def _get_tag(self, tag_name: Optional[str], special_tag: SpecialTag) -> Tag:
        if tag_name is None:
            return special_tag
        for t in self.get_tags():
            if t.name == tag_name:
                return t
        raise Exception("tag: %s not found" % tag_name)

    def get_tag1(self, tag_name: Optional[str]) -> Tag:
        return self._get_tag(tag_name, BeginningTag())

    def get_tag2(self, tag_name: Optional[str]) -> Tag:
        return self._get_tag(tag_name, HeadTag())

    def get_first_commit(self) -> Commit:
        return self.backend.get_first_commit()

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        return self.backend.get_commits_between(tag1, tag2)

    def get_commits(self) -> List[Commit]:
        return self.get_commits_between(BeginningTag(), HeadTag())
