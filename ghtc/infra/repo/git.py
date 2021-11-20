import datetime
from typing import List, Optional, Tuple

from git import Repo as GitRepo
from git.objects.commit import Commit as GitCommit

from ghtc.app.repo import RepoBackendInterface
from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, Tag


class RepoGitBackend(RepoBackendInterface):
    def __init__(self, repo_root: str):
        self.repo_root: str = repo_root
        self.repo: GitRepo = GitRepo(repo_root)

    def get_all_tags(self) -> List[Tag]:
        res: List[Tag] = []
        for tag in self.repo.tags:
            res.append(
                Tag(
                    name=tag.name,
                    date=datetime.datetime.utcfromtimestamp(tag.object.authored_date),
                )
            )
        return res

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

    def _tag_to_revision(self, tag: Tag) -> Tuple[str, bool]:
        if isinstance(tag, HeadTag):
            return "HEAD", True
        elif isinstance(tag, BeginningTag):
            res: Optional[str] = None
            tmp_tags = self.get_all_tags()
            for t in tmp_tags:
                if t.name.startswith("ghtc_changelog_start"):
                    res = t.name
            if res is None:
                return self.get_first_commit().hexsha, True
            return res, False
        return tag.name, False

    def get_commits_between(self, tag1: Tag, tag2: Tag) -> List[Commit]:
        kwargs = {}
        tag1_name, return_first_commit = self._tag_to_revision(tag1)
        tag2_name, _ = self._tag_to_revision(tag2)
        kwargs["rev"] = f"{tag1_name}..{tag2_name}"
        tmp = list(self.repo.iter_commits(**kwargs))
        if not return_first_commit:
            return self._convert_commits(tmp)
        return [self.get_first_commit()] + self._convert_commits(tmp)
