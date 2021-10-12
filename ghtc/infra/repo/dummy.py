from typing import List

from ghtc.app.repo import RepoBackendInterface
from ghtc.domain.commit import Commit
from ghtc.domain.tag import Tag


class RepoDummyBackend(RepoBackendInterface):
    def __init__(self, tags: List[Tag], commits: List[Commit]):
        self.tags: List[Tag] = tags
        self.commits: List[Commit] = sorted(commits, key=lambda x: x.committed_date)

    def get_tags(self) -> List[Tag]:
        return self.tags

    def get_first_commit(self) -> Commit:
        return self.commits[0]

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        return [
            x
            for x in self.commits
            if x.committed_date > tag1.tagged_date
            and x.committed_date <= tag2.tagged_date
        ]
