from typing import Dict, Optional

from ghtc.app.override import OverrideBackendInterface
from ghtc.domain.commit import ConventionalCommitMessage


class OverrideDummyBackend(OverrideBackendInterface):
    def __init__(self, overrides: Dict[str, ConventionalCommitMessage]):
        self.overrides = overrides

    def get_override(self, hexsha: str) -> Optional[ConventionalCommitMessage]:
        return self.overrides.get(hexsha)
