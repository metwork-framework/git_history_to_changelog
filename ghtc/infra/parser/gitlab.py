from typing import List, Optional

from ghtc.app.parser import ParserBackendInterface
from ghtc.domain.changelog import ChangelogEntry, ChangelogEntryType


class ParserGitlabBackend(ParserBackendInterface):
    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        if not commit_message:
            return []
        type: Optional[ChangelogEntryType] = None
        lines = commit_message.splitlines()
        empty_line_found: bool = False
        for line in lines:
            if line.strip() == "":
                empty_line_found = True
            elif line.startswith("Changelog:") and empty_line_found:
                tmp = line.split(":", 1)[1].strip().upper()
                if tmp in ChangelogEntryType:
                    type = ChangelogEntryType[tmp]
        if type is None:
            return []
        return [
            ChangelogEntry(
                type=type,
                message=lines[0].strip(),
            )
        ]

    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        return None
