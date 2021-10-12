from typing import List, Optional, cast

from ghtc.app.override import OverrideController
from ghtc.app.parser import get_reverted_commit, parse
from ghtc.app.repo import RepoController
from ghtc.domain.changelog import Changelog, ChangelogLine, ChangelogSection
from ghtc.domain.commit import ConventionalCommitMessage, ConventionalCommitType
from ghtc.domain.tag import BeginningTag, HeadTag, Tag


class ChangelogController:
    def __init__(
        self,
        repo: RepoController,
        override: OverrideController,
        tags_regex=".*",
        commit_types: List[ConventionalCommitType] = [
            x for x in ConventionalCommitType
        ],
        unreleased: bool = True,
    ):
        self.repo: RepoController = repo
        self.override: OverrideController = override
        self.tags: List[Tag] = [cast(Tag, BeginningTag())] + self.repo.get_tags(
            tags_regex
        )
        self.reverteds: List[str] = [
            y
            for y in [get_reverted_commit(x.message) for x in self.repo.get_commits()]
            if y is not None
        ]
        self.commit_types: List[ConventionalCommitType] = commit_types
        self.unreleased = unreleased
        if self.unreleased:
            self.tags.append(HeadTag())

    def get_changelog(
        self, starting_tag: Tag, ending_tag: Tag, tags_regex=".*"
    ) -> Changelog:
        res: Changelog = Changelog()
        for i in range(1, len(self.tags)):
            chapter = self.get_changelog_chapter(self.tags[i - 1], self.tags[i])
            res.chapters.append(chapter)
        return res

    def get_changelog_chapter(self, previous_tag: Tag, tag: Tag) -> ChangelogSection:
        res: ChangelogSection = ChangelogSection(tag=tag)
        line: ChangelogLine
        for commit in self.repo.get_commits_between(previous_tag, tag):
            if commit.hexsha in self.reverteds:
                continue
            cm: Optional[ConventionalCommitMessage] = self.override.get_override(
                commit.hexsha
            )
            if cm is None:
                cm = parse(commit.message)
                if cm is None:
                    continue
            if cm.type not in self.commit_types:
                continue
            line = ChangelogLine(
                commit_message=cm,
                commit_sha=commit.hexsha,
                commit_date=commit.committed_date,
            )
            res.add_line(line)
        return res
