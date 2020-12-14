from typing import Any, Dict, List, Optional
import typer
from git import Repo
from ghtc.utils import (
    get_tags,
    get_commits_between,
    get_tag,
    render_template,
    get_reverted_commit,
)
from ghtc.models import (
    ChangelogLine,
    ChangelogEntryForATag,
    ConventionalCommitMessage,
    ConventionalCommitType,
    UNRELEASED_TAG_TIMESTAMP,
)
from ghtc.parser import parse


def main(
    repo_root: str,
    tags_regex: str = "^v[0-9]",
    starting_tag: str = None,
    remove_duplicates_entries=True,
    unreleased=True,
    include_type: List[str] = [],
    title: str = "CHANGELOG",
    unreleased_title="[Unreleased]",
):
    repo = Repo(repo_root)
    previous_tag = get_tag(repo, starting_tag)
    context: Dict[str, Any] = {
        "TITLE": title,
        "UNRELEASED_TAG_TIMESTAMP": UNRELEASED_TAG_TIMESTAMP,
        "TAGS": [],
    }
    tags = get_tags(repo, tags_regex)
    if len(include_type) == 0:
        # if include_type is empty, we consider we want all types
        included_cats = [x.name.lower() for x in list(ConventionalCommitType)]
    else:
        included_cats = [x.strip().lower() for x in include_type]
    if unreleased:
        tags.append(None)
    for tag in tags:
        if tag is None:
            tag_name = unreleased_title
            tag_date = UNRELEASED_TAG_TIMESTAMP
        else:
            tag_name = tag.name
            tag_date = tag.object.authored_date
        reverted_commits = []
        for commit in get_commits_between(repo, previous_tag, tag):
            reverted_commit = get_reverted_commit(commit)
            if reverted_commit is not None:
                reverted_commits.append(reverted_commit)
        lines: Dict[ConventionalCommitType, List[ChangelogLine]] = {}
        for commit in get_commits_between(repo, previous_tag, tag):
            if commit.hexsha in reverted_commits:
                continue
            msg: Optional[ConventionalCommitMessage] = parse(commit.message)
            if msg is None:
                continue
            cat = msg.type
            if cat.name.lower() not in included_cats:
                continue
            cline = ChangelogLine(msg, commit.hexsha, commit.committed_date)
            if cat not in lines:
                lines[cat] = []
            if remove_duplicates_entries and cline in lines[cat]:
                continue
            lines[cat].insert(0, cline)
        entry = ChangelogEntryForATag(tag_name, tag_date, lines)
        context["TAGS"].append(entry)
        previous_tag = tag
    print(render_template(context))


if __name__ == "__main__":
    typer.run(main)
