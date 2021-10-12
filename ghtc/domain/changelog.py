import datetime
from typing import List

from pydantic import BaseModel, Field

from ghtc.domain.commit import ConventionalCommitMessage, ConventionalCommitType
from ghtc.domain.tag import Tag


UNRELEASED_TAG_TIMESTAMP = 9999999999


class ChangelogLine(BaseModel):

    commit_message: ConventionalCommitMessage
    commit_sha: str
    commit_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class ChangelogSubSection(BaseModel):

    typ: ConventionalCommitType
    lines: List[ChangelogLine] = Field(default_factory=list)


class ChangelogSection(BaseModel):

    tag: Tag
    subsections: List[ChangelogSubSection] = Field(default_factory=list)

    def tag_date(self) -> str:
        return self.tag.tagged_date.strftime("%Y-%m-%d")

    def get_or_make_subsection(
        self, typ: ConventionalCommitType
    ) -> ChangelogSubSection:
        for s in self.subsections:
            if s.typ == typ:
                return s
        s = ChangelogSubSection(typ=typ)
        self.subsections.append(s)
        return s

    def add_line(self, line: ChangelogLine) -> None:
        s = self.get_or_make_subsection(line.commit_message.type)
        s.lines.append(line)


class Changelog(BaseModel):

    chapters: List[ChangelogSection] = Field(default_factory=list)
