import datetime
from typing import List

from ghtc.app.repo import RepoBackendInterface
from ghtc.domain.commit import Commit
from ghtc.domain.tag import Tag


class RepoDummyBackend(RepoBackendInterface):
    def __init__(self, tags: List[Tag], commits: List[Commit]):
        self.tags: List[Tag] = tags
        self.commits: List[Commit] = sorted(commits, key=lambda x: x.date)

    def get_tags_between(self, tag1: Tag, tag2: Tag) -> List[Tag]:
        d1: datetime.datetime = tag1.date
        d2: datetime.datetime = tag2.date
        return [x for x in self.tags if x.date >= d1 and x.date <= d2]

    def get_first_commit(self) -> Commit:
        return self.commits[0]

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        return [x for x in self.commits if x.date > tag1.date and x.date <= tag2.date]
