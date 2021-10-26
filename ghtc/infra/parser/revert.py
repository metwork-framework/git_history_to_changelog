from typing import List, Optional

from ghtc.app.parser import ParserBackendInterface
from ghtc.domain.changelog import ChangelogEntry


class ParserRevertBackend(ParserBackendInterface):
    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        return []

    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        for tmp in commit_message.splitlines():
            line = tmp.strip()
            if line.startswith("This reverts commit "):
                sha = line.replace("This reverts commit ", "").split(".")[0]
                if len(sha) >= 40:
                    return sha
            if line.startswith("Revert:"):
                sha = line.replace("Revert:", "").strip()
                if len(sha) >= 40:
                    return sha
        return None
