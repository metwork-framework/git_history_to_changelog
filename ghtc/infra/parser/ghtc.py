from typing import List, Optional, Tuple

from ghtc.app.parser import ParserBackendInterface
from ghtc.domain.changelog import ChangelogEntry, ChangelogEntryType
from ghtc.infra.parser.conventional import TYPE_MAPPINGS


BEGINNING_TAG = "<changelog>"
ENDING_TAG = "</changelog>"


class ParserGhtcBackend(ParserBackendInterface):
    def _parse_first_cle(
        self, commit_message: str, start_index: int
    ) -> Optional[Tuple[ChangelogEntry, int]]:
        if not commit_message:
            return None
        start: int = commit_message.find(BEGINNING_TAG, start_index)
        if start < 0:
            return None
        end: int = commit_message.find(ENDING_TAG, start)
        if end < 0:
            return None
        start2: int = start + len(BEGINNING_TAG)
        tmp = commit_message[start2:end].strip().replace("\r", " ").replace("\n", " ")
        type: Optional[ChangelogEntryType] = None
        lowered_tmp: str = tmp.lower()
        for x in list(ChangelogEntryType):
            if lowered_tmp.startswith(x.name.lower() + ":"):
                type = x
                break
        if type is None:
            for y in TYPE_MAPPINGS.keys():
                if lowered_tmp.startswith(y + ":"):
                    type = TYPE_MAPPINGS[y]
        if type is None:
            return None
        return (
            ChangelogEntry(type=type, message=tmp.split(":", 1)[1].strip()),
            end + len(ENDING_TAG),
        )

    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        res: List[ChangelogEntry] = []
        cle: ChangelogEntry
        start_index: int = 0
        while True:
            tmp: Optional[Tuple[ChangelogEntry, int]] = self._parse_first_cle(
                commit_message, start_index
            )
            if tmp is None:
                break
            cle, start_index = tmp
            res.append(cle)
        return res

    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        return None
