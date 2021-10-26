from ghtc.domain.changelog import ChangelogEntry, ChangelogEntryType, ChangelogSection
from ghtc.domain.tag import HeadTag


def test_changelog():
    x = ChangelogSection(tag=HeadTag())
    a = ChangelogEntry(
        type=ChangelogEntryType.ADDED,
        message="foo",
        commit_sha="123",
    )
    b = ChangelogEntry(
        type=ChangelogEntryType.FIXED,
        message="foo2",
        commit_sha="1234",
    )
    x.add_line(a)
    x.add_line(a)
    x.add_line(b)
    assert len(x.subsections) == 2
    fixes = [i for i in x.subsections if i.type == ChangelogEntryType.FIXED][0]
    feats = [i for i in x.subsections if i.type == ChangelogEntryType.ADDED][0]
    assert len(fixes.lines) == 1
    assert len(feats.lines) == 2
