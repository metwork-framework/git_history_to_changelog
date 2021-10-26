from typing import Dict, List

from ghtc.app.override import OverrideBackendInterface
from ghtc.domain.changelog import ChangelogEntry


class OverrideDummyBackend(OverrideBackendInterface):
    def __init__(self, overrides: Dict[str, List[ChangelogEntry]] = {}):
        self.overrides = overrides

    def get_override(self, hexsha: str) -> List[ChangelogEntry]:
        return self.overrides.get(hexsha, [])
