from typing import List, Optional

from ghtc.app.parser import ParserBackendInterface
from ghtc.domain.changelog import ChangelogEntry, ChangelogEntryType
from ghtc.infra.parser.conventional import ParserConventionalBackend


MSG1 = """feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other files
"""

MSG2 = """refactor!: drop support for Node 6"""

MSG3 = """refactor!: drop support for Node 6

BREAKING CHANGE: refactor to use JavaScript features not available in Node 6.
"""

MSG4 = """docs: correct spelling of CHANGELOG"""

MSG5 = """feat(lang): add polish language"""

MSG6 = """fix: correct minor typos in code

see the issue for details

on typos fixed.

Reviewed-by: Z
Refs #133
"""


class SingleEntryAdapter:
    def __init__(self, backend: ParserBackendInterface):
        self.backend = backend

    def parse(self, commit_message: str) -> Optional[ChangelogEntry]:
        tmp: List[ChangelogEntry] = self.backend.parse(commit_message)
        if len(tmp) == 0:
            return None
        if len(tmp) > 1:
            raise Exception("too many changelog entries returned")
        return tmp[0]


parser = SingleEntryAdapter(ParserConventionalBackend())


def test_valid_messages():

    msg = parser.parse(MSG1)
    assert msg.type == ChangelogEntryType.ADDED
    assert msg.message == "allow provided config object to extend other configs"
    msg = parser.parse(MSG2)
    assert msg.type == ChangelogEntryType.CHANGED
    assert msg.message == "drop support for Node 6"
    msg = parser.parse(MSG3)
    assert msg.type == ChangelogEntryType.CHANGED
    assert msg.message == "drop support for Node 6"
    msg = parser.parse(MSG4)
    assert msg.type == ChangelogEntryType.OTHER
    assert msg.message == "correct spelling of CHANGELOG"
    msg = parser.parse(MSG5)
    assert msg.type == ChangelogEntryType.ADDED
    assert msg.message == "(lang) add polish language"
    msg = parser.parse(MSG6)
    assert msg.type == ChangelogEntryType.FIXED
    assert msg.message == "correct minor typos in code"
