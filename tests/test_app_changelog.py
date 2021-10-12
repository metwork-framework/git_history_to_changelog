import datetime
from typing import List

from ghtc.app.changelog import ChangelogController
from ghtc.app.override import OverrideController
from ghtc.app.repo import RepoController
from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, Tag
from ghtc.infra.override.dummy import OverrideDummyBackend
from ghtc.infra.repo.dummy import RepoDummyBackend


tags: List[Tag] = [
    Tag(name="0.1.0", tagged_date=datetime.datetime(2020, 1, 1)),
    Tag(name="0.2.0", tagged_date=datetime.datetime(2020, 2, 12)),
    Tag(name="0.2.1", tagged_date=datetime.datetime(2020, 2, 13)),
]
commits: List[Commit] = []


def test_changelog():
    r = RepoController(RepoDummyBackend(tags, commits))
    o = OverrideController(OverrideDummyBackend([]))
    a = ChangelogController(repo=r, override=o)
    a.get_changelog(BeginningTag(), HeadTag())
