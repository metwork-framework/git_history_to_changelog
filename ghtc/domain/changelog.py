import datetime
from enum import Enum, auto
from typing import List, Optional

from pydantic import BaseModel, Field

from ghtc.domain.tag import Tag


UNRELEASED_TAG_TIMESTAMP = 9999999999


class ChangelogEntryType(Enum):

    ADDED = auto()
    FIXED = auto()
    CHANGED = auto()
    DEPRECATED = auto()
    REMOVED = auto()
    SECURITY = auto()
    PERFORMANCE = auto()
    OTHER = auto()


class ChangelogEntry(BaseModel):

    type: ChangelogEntryType
    message: str
    commit_sha: Optional[str] = None
    links: List[str] = Field(default_factory=list)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class ChangelogSubSection(BaseModel):

    type: ChangelogEntryType
    lines: List[ChangelogEntry] = Field(default_factory=list)


class ChangelogSection(BaseModel):

    tag: Tag
    subsections: List[ChangelogSubSection] = Field(default_factory=list)

    def tag_date(self) -> str:
        return self.tag.date.strftime("%Y-%m-%d")

    def get_subsection_by_type(
        self, type: ChangelogEntryType
    ) -> Optional[ChangelogSubSection]:
        for s in self.subsections:
            if s.type == type:
                return s
        return None

    def _get_or_make_subsection(self, type: ChangelogEntryType) -> ChangelogSubSection:
        s: Optional[ChangelogSubSection] = self.get_subsection_by_type(type)
        if s is not None:
            return s
        s = ChangelogSubSection(type=type)
        self.subsections.append(s)
        return s

    def add_line(self, line: ChangelogEntry) -> None:
        s = self._get_or_make_subsection(line.type)
        s.lines.append(line)


class Changelog(BaseModel):

    sections: List[ChangelogSection] = Field(default_factory=list)

    def get_section_by_tag_name(self, tag_name: str) -> Optional[ChangelogSection]:
        for s in self.sections:
            if s.tag.name == tag_name:
                return s
        return None
