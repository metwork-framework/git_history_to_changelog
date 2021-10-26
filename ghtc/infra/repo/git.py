import datetime
from typing import List, Optional

from git import Repo as GitRepo
from git.objects.commit import Commit as GitCommit

from ghtc.app.repo import RepoBackendInterface
from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, Tag


class RepoGitBackend(RepoBackendInterface):
    def __init__(self, repo_root: str):
        self.repo_root: str = repo_root
        self.repo: GitRepo = GitRepo(repo_root)

    def get_tags_between(self, tag1: Tag, tag2: Tag) -> List[Tag]:
        res: List[Tag] = []
        kwargs = {"rev": f"{tag1.name}..{tag2.name}"}
        for commit in self.repo.iter_commits(**kwargs):
            for tag in self.repo.tags:
                if commit.hexsha == tag.commit.hexsha:
                    res.append(
                        Tag(
                            name=tag.name,
                            date=datetime.datetime.utcfromtimestamp(
                                tag.object.authored_date
                            ),
                        )
                    )
        return res

    def get_tags(self) -> List[Tag]:
        first_commit = self.get_first_commit()
        tag1 = Tag(name=first_commit.hexsha, date=first_commit.date)
        tag2 = HeadTag()
        return self.get_tags_between(tag1, tag2)

    def get_first_commit(self) -> Commit:
        x: GitCommit = list(self.repo.iter_commits(max_parents=0))[0]
        return self._convert_commit(x)

    def _convert_commit(self, commit: GitCommit) -> Commit:
        return Commit(
            hexsha=commit.hexsha,
            date=datetime.datetime.utcfromtimestamp(commit.committed_date),
            message=commit.message,
        )

    def _convert_commits(self, commits: List[GitCommit]) -> List[Commit]:
        return [self._convert_commit(x) for x in commits]

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        kwargs = {}
        tag1_name: Optional[str] = None
        tag2_name: str
        return_first_commit: bool = False
        if isinstance(tag1, BeginningTag):
            tmp_tags = self.get_tags()
            for t in tmp_tags:
                if t.name.startswith("ghtc_changelog_start"):
                    tag1_name = t.name
            if tag1_name is None:
                tag1_name = self.get_first_commit().hexsha
                return_first_commit = True
        else:
            tag1_name = tag1.name
        if isinstance(tag2, HeadTag):
            tag2_name = "HEAD"
        else:
            tag2_name = tag2.name
        kwargs["rev"] = f"{tag1_name}..{tag2_name}"
        tmp = list(self.repo.iter_commits(**kwargs))
        if not return_first_commit:
            return self._convert_commits(tmp)
        return [self.get_first_commit()] + self._convert_commits(tmp)
