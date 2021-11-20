import os
import re
from collections import defaultdict
from typing import Dict, List, Optional

import mflog

from ghtc.app.override import OverrideBackendInterface
from ghtc.app.parser import ParserController
from ghtc.domain.changelog import ChangelogEntry


GIT_COMMIT_DELIMITER_REGEX = r"^\[([0-9a-f]{5,40})\]$"
GIT_COMMIT_DELIMITER_COMPILED_REGEX = re.compile(GIT_COMMIT_DELIMITER_REGEX)
LOGGER = mflog.get_logger("ghtc.overrides")


class OverrideInifileBackend(OverrideBackendInterface):
    def __init__(self, path, parserc: ParserController):
        self.path = path
        self.overrides: Dict[str, List[ChangelogEntry]] = defaultdict(list)
        self.parserc = parserc
        self.parse()

    def get_override(self, hexsha: str) -> List[ChangelogEntry]:
        return self.overrides.get(hexsha, [])

    def parse(self) -> bool:
        if not os.path.isfile(self.path):
            return False
        with open(self.path, "r") as f:
            commit: Optional[str] = None
            commit_message: Optional[str] = None
            for tmp in f.readlines():
                line = tmp.strip()
                if commit is None and len(line) == 0:
                    continue
                match = GIT_COMMIT_DELIMITER_COMPILED_REGEX.match(line)
                if match is None:
                    if commit is None:
                        LOGGER.warning("badly formatted overrides file => ignoring")
                        return False
                    if commit_message is None:
                        if len(line) > 0:
                            commit_message = line
                    else:
                        commit_message = commit_message + "\n" + line
                else:
                    if commit is not None:
                        self.overrides[commit] = self.overrides[commit] + self._parse(
                            commit_message
                        )
                    commit = match[1]
                    commit_message = None
            if commit is not None:
                self.overrides[commit] = self.overrides[commit] + self._parse(
                    commit_message
                )
        return True

    def _parse(self, commit_message: Optional[str]) -> List[ChangelogEntry]:
        if commit_message is not None:
            return self.parserc.parse(commit_message)
        return []
