from ghtc.domain.changelog import ChangelogEntryType
from ghtc.infra.parser.ghtc import ParserGhtcBackend


MSG1 = """
title

<changelog>feat: this is a basic test</changelog>

trailer: foo
"""

MSG2 = """
title

foo <changelog>feat: foo
bar  </changelog>

trailer: foo
"""

parser = ParserGhtcBackend()


def test_valid_messages():

    msgs = parser.parse(MSG1)
    assert len(msgs) == 1
    assert msgs[0].type == ChangelogEntryType.ADDED
    assert msgs[0].message == "this is a basic test"

    msgs = parser.parse(MSG2)
    assert len(msgs) == 1
    assert msgs[0].type == ChangelogEntryType.ADDED
    assert msgs[0].message == "foo bar"
