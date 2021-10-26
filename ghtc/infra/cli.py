import os
from typing import List, Optional

import jinja2
from devtools import debug as debug_print
from typer import Argument, Option, Typer

from ghtc.app.changelog import ChangelogController
from ghtc.app.override import OverrideController
from ghtc.app.parser import ParserController
from ghtc.app.repo import RepoController
from ghtc.domain.changelog import ChangelogEntryType
from ghtc.domain.tag import Tag
from ghtc.infra.override.dummy import OverrideDummyBackend
from ghtc.infra.parser.conventional import ParserConventionalBackend
from ghtc.infra.parser.revert import ParserRevertBackend
from ghtc.infra.repo.git import RepoGitBackend


app = Typer(add_completion=False)
ALL_TYPES = ", ".join([x.name.lower() for x in ChangelogEntryType])
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DEFAULT_FILE = os.path.join(CURRENT_DIR, "..", "templates", "CHANGELOG.md")


@app.command()
def cli(
    repo_root: str = Argument(..., help="the fullpath to the git repository"),
    tags_regex: str = Option(
        "^v[0-9]", help="regex to select tags to show on changelog"
    ),
    starting_rev: str = Option(
        None,
        help="starting revision (if not set latest tag starting with "
        "ghtc_changelog_start if exists, else first git commit)",
    ),
    remove_duplicates_entries: bool = Option(
        True, help="if True, remove duplicate entries"
    ),
    unreleased: bool = Option(
        True, help="if True, add a section about unreleased changes"
    ),
    override_file: str = Option(
        ".ghtc_overrides.ini", help="the path/name of the 'commit overrides' file"
    ),
    include_type: List[str] = Option(
        [],
        help="include (only) given conventional types in changelog (can be used "
        "multiple times), available types: %s" % ALL_TYPES,
    ),
    title: str = "CHANGELOG",
    unreleased_title: str = "[Unreleased]",
    debug: bool = Option(False, help="add debug values for each changelog entry"),
    template_file: Optional[str] = Option(None, help="use an alternate template file"),
):
    included_cats: List[ChangelogEntryType] = [
        x for x in list(ChangelogEntryType) if x != ChangelogEntryType.OTHER
    ]
    if len(include_type) > 0:
        included_cats = [
            x for x in list(ChangelogEntryType) if x.name.lower() in include_type
        ]
    x = ChangelogController(
        repo=RepoController(RepoGitBackend(repo_root)),
        parser=ParserController([ParserRevertBackend(), ParserConventionalBackend()]),
        override=OverrideController(OverrideDummyBackend()),
        tags_regex=tags_regex,
        commit_types=included_cats,
        unreleased=unreleased,
    )
    tag1: Tag = x.repo.get_tag1(starting_rev)
    tag2: Tag
    if unreleased:
        tag2 = x.repo.get_tag2(None)
    else:
        tag2 = x.repo.get_tags()[-1]
    c = x.get_changelog(tag1, tag2)
    debug_print(c)
    if template_file is not None:
        template_to_read = template_file
    else:
        template_to_read = TEMPLATE_DEFAULT_FILE
    with open(template_to_read, "r") as f:
        content = f.read()
    template = jinja2.Template(content)
    context = {"CHANGELOG": c, "TITLE": title, "UNRELEASED_TITLE": unreleased_title}
    print(template.render(context))


def main():
    app()


if __name__ == "__main__":
    main()
