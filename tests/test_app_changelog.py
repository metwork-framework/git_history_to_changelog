import datetime
from typing import List

from ghtc.app.changelog import ChangelogController
from ghtc.app.override import OverrideController
from ghtc.app.parser import ParserController
from ghtc.app.repo import RepoController
from ghtc.domain.changelog import ChangelogEntryType
from ghtc.domain.commit import Commit
from ghtc.domain.tag import BeginningTag, HeadTag, Tag
from ghtc.infra.override.dummy import OverrideDummyBackend
from ghtc.infra.parser.conventional import ParserConventionalBackend
from ghtc.infra.parser.revert import ParserRevertBackend
from ghtc.infra.repo.dummy import RepoDummyBackend


tags: List[Tag] = [
    Tag(name="0.1.0", date=datetime.datetime(2020, 1, 1)),
    Tag(name="0.2.0", date=datetime.datetime(2020, 2, 12)),
    Tag(name="0.2.1", date=datetime.datetime(2020, 2, 13)),
]
commits: List[Commit] = [
    Commit(
        hexsha="1234", date=datetime.datetime(2019, 7, 3), message="feat: foo"
    ),  # => 0.1.0
    Commit(
        hexsha="789", date=datetime.datetime(2019, 7, 5), message="fix: bar"
    ),  # => 0.1.0
    Commit(
        hexsha="aabbb",
        date=datetime.datetime(2020, 2, 13),
        message="feat: foobar",
    ),  # => 0.2.1
    Commit(
        hexsha="bbccdd",
        date=datetime.datetime(2021, 2, 13),
        message="feat: foobar2",
    ),  # => 0.2.1
]


def test_changelog():
    r = RepoController(RepoDummyBackend(tags, commits))
    o = OverrideController(OverrideDummyBackend({}))
    p = ParserController([ParserRevertBackend(), ParserConventionalBackend()])
    a = ChangelogController(repo=r, override=o, parser=p)
    c = a.get_changelog(BeginningTag(), HeadTag())
    assert len(c.sections) == 4
    assert len(c.get_section_by_tag_name("0.1.0").subsections) == 2
    c.get_section_by_tag_name("0.1.0").get_subsection_by_type(
        ChangelogEntryType.ADDED
    ).lines[0].message == "foo"
    c.get_section_by_tag_name("0.1.0").get_subsection_by_type(
        ChangelogEntryType.FIXED
    ).lines[0].message == "bar"
    assert len(c.get_section_by_tag_name("0.2.0").subsections) == 0
    assert len(c.get_section_by_tag_name("0.2.1").subsections) == 1
    c.get_section_by_tag_name("0.2.1").get_subsection_by_type(
        ChangelogEntryType.ADDED
    ).lines[0].message == "foobar"
    assert len(c.get_section_by_tag_name("__head").subsections) == 1
    c.get_section_by_tag_name("__head").get_subsection_by_type(
        ChangelogEntryType.ADDED
    ).lines[0].message == "foobar2"
