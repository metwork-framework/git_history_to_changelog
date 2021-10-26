import re
from typing import Dict, List, Optional, Tuple

from ghtc.app.parser import ParserBackendInterface
from ghtc.domain.changelog import ChangelogEntry, ChangelogEntryType


TYPE_MAPPINGS: Dict[str, ChangelogEntryType] = {
    "feat": ChangelogEntryType.ADDED,
    "fix": ChangelogEntryType.FIXED,
    "build": ChangelogEntryType.OTHER,
    "chore": ChangelogEntryType.OTHER,
    "ci": ChangelogEntryType.OTHER,
    "docs": ChangelogEntryType.OTHER,
    "doc": ChangelogEntryType.OTHER,
    "style": ChangelogEntryType.OTHER,
    "refactor": ChangelogEntryType.OTHER,
    "perf": ChangelogEntryType.PERFORMANCE,
    "perfs": ChangelogEntryType.PERFORMANCE,
    "test": ChangelogEntryType.OTHER,
    "tests": ChangelogEntryType.OTHER,
    "security": ChangelogEntryType.SECURITY,
    "deprecated": ChangelogEntryType.DEPRECATED,
    "removed": ChangelogEntryType.REMOVED,
}
TITLE_REGEX = r"^([a-zA-Z0-9_-]+)(!{0,1})(\([a-zA-Z0-9_-]*\)){0,1}(!{0,1}): (.*)$"
TITLE_COMPILED_REGEX = re.compile(TITLE_REGEX)
FOOTER_REGEX1 = r"^([a-zA-Z0-9_-]+): (.*)$"
FOOTER_COMPILED_REGEX1 = re.compile(FOOTER_REGEX1)
FOOTER_REGEX2 = r"^([a-zA-Z0-9_-]+) #(.*)$"
FOOTER_COMPILED_REGEX2 = re.compile(FOOTER_REGEX2)
BREAKING_CHANGE_FOOTER_REGEX = r"^BREAKING[- ]CHANGE: (.*)$"
BREAKING_CHANGE_FOOTER_COMPILED_REGEX = re.compile(BREAKING_CHANGE_FOOTER_REGEX)


class ParserConventionalBackend(ParserBackendInterface):
    def type_string_to_commit_type(
        self, type_str: str, breaking: bool
    ) -> ChangelogEntryType:
        res: ChangelogEntryType = ChangelogEntryType.OTHER
        if type_str in TYPE_MAPPINGS:
            res = TYPE_MAPPINGS[type_str]
        if breaking:
            if res not in (
                ChangelogEntryType.ADDED,
                ChangelogEntryType.FIXED,
                ChangelogEntryType.REMOVED,
            ):
                return ChangelogEntryType.CHANGED
        return res

    def parse(self, commit_message: str) -> List[ChangelogEntry]:
        if not commit_message:
            return []
        lines = commit_message.splitlines()
        first_line = lines[0]
        match = TITLE_COMPILED_REGEX.match(first_line)
        if match is None:
            return []
        type_str = match[1].lower()
        breaking = False
        if match[2] or match[4]:
            breaking = True
        scope = None
        if match[3]:
            scope = match[3].lower()[1:-1]
        description = match[5]
        body = None
        footers: List[Tuple[str, str]] = []
        if len(lines) > 1 and lines[1] == "":
            for line in lines[1:]:
                if not line:
                    continue
                tmp1 = FOOTER_COMPILED_REGEX1.match(line)
                tmp2 = FOOTER_COMPILED_REGEX2.match(line)
                tmp3 = BREAKING_CHANGE_FOOTER_COMPILED_REGEX.match(line)
                if len(footers) == 0 and tmp1 is None and tmp2 is None and tmp3 is None:
                    if body is None:
                        body = f"{line}"
                    else:
                        body += f"\n{line}"
                else:
                    if tmp3 is not None:
                        breaking = True
                        footers.append(("BREAKING CHANGE", tmp3[1]))
                    elif tmp1 is not None:
                        footers.append((tmp1[1], tmp1[2]))
                    elif tmp2 is not None:
                        footers.append((tmp2[1], tmp2[2]))
        msg: str = description
        if scope is not None:
            msg = "(%s) %s" % (scope, description)
        return [
            ChangelogEntry(
                type=self.type_string_to_commit_type(type_str, breaking),
                message=msg,
            )
        ]

    def get_reverted_commit(self, commit_message: str) -> Optional[str]:
        return None
