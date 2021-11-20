from ghtc.domain.changelog import ChangelogEntryType
from ghtc.infra.parser.gitlab import ParserGitlabBackend


MSG1 = """this is a test
"""

MSG2 = """this is a test

Changelog: added
"""


parser = ParserGitlabBackend()


def test_valid_messages():

    msgs = parser.parse(MSG2)
    assert len(msgs) == 1
    assert msgs[0].type == ChangelogEntryType.ADDED
    assert msgs[0].message == "this is a test"


def test_invalid_messages():

    msgs = parser.parse(MSG1)
    assert len(msgs) == 0
