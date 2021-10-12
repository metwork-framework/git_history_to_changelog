from ghtc.domain.changelog import ChangelogLine, ChangelogSection
from ghtc.domain.commit import ConventionalCommitMessage, ConventionalCommitType
from ghtc.domain.tag import HeadTag


def test_changelog():
    x = ChangelogSection(tag=HeadTag())
    a = ChangelogLine(
        commit_message=ConventionalCommitMessage(
            type=ConventionalCommitType.FEAT, description="foo"
        ),
        commit_sha="123",
    )
    b = ChangelogLine(
        commit_message=ConventionalCommitMessage(
            type=ConventionalCommitType.FIX, description="foo2"
        ),
        commit_sha="1234",
    )
    x.add_line(a)
    x.add_line(a)
    x.add_line(b)
    assert len(x.subsections) == 2
    fixes = [i for i in x.subsections if i.typ == ConventionalCommitType.FIX][0]
    feats = [i for i in x.subsections if i.typ == ConventionalCommitType.FEAT][0]
    assert len(fixes.lines) == 1
    assert len(feats.lines) == 2
