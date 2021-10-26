from typing import List, cast

from ghtc.app.override import OverrideController
from ghtc.app.parser import ParserController
from ghtc.app.repo import RepoController
from ghtc.domain.changelog import (
    Changelog,
    ChangelogEntry,
    ChangelogEntryType,
    ChangelogSection,
)
from ghtc.domain.tag import BeginningTag, HeadTag, Tag


class ChangelogController:
    def __init__(
        self,
        repo: RepoController,
        parser: ParserController,
        override: OverrideController,
        tags_regex=".*",
        commit_types: List[ChangelogEntryType] = [x for x in ChangelogEntryType],
        unreleased: bool = True,
    ):
        self.repo: RepoController = repo
        self.parser: ParserController = parser
        self.override: OverrideController = override
        self.tags: List[Tag] = [cast(Tag, BeginningTag())] + self.repo.get_tags(
            tags_regex
        )
        self.reverteds: List[str] = [
            y
            for y in [
                self.parser.get_reverted_commit(x.message)
                for x in self.repo.get_commits()
            ]
            if y is not None
        ]
        self.commit_types: List[ChangelogEntryType] = commit_types
        self.unreleased = unreleased
        if self.unreleased:
            self.tags.append(HeadTag())

    def get_tags(self, starting_tag: Tag, ending_tag: Tag) -> List[Tag]:
        # FIXME !!!
        return self.tags

    def get_changelog(self, starting_tag: Tag, ending_tag: Tag) -> Changelog:
        res: Changelog = Changelog()
        for i in range(1, len(self.get_tags(starting_tag, ending_tag))):
            chapter = self.get_changelog_chapter(self.tags[i - 1], self.tags[i])
            res.sections.append(chapter)
        return res

    def get_changelog_chapter(self, previous_tag: Tag, tag: Tag) -> ChangelogSection:
        res: ChangelogSection = ChangelogSection(tag=tag)
        for commit in self.repo.get_commits_between(previous_tag, tag):
            if commit.hexsha in self.reverteds:
                continue
            cles: List[ChangelogEntry] = self.override.get_override(commit.hexsha)
            if len(cles) == 0:
                cles = self.parser.parse(commit.message)
                if len(cles) == 0:
                    continue
            for cle in cles:
                if cle.type not in self.commit_types:
                    continue
                cle.date = commit.date
                cle.commit_sha = commit.hexsha
                res.add_line(cle)
        return res
