from typing import Any, Dict, Optional, List
import typer
from ghtc.utils import get_tags, get_commits_between, get_tag, render_template
from git import Repo


def main(
    repo_root: str,
    tags_regex: str = "^v[0-9]",
    starting_tag: str = None,
    remove_duplicates_entries=True,
    unreleased=True,
):
    repo = Repo(repo_root)
    previous_tag = get_tag(repo, starting_tag)
    context: Dict[str, Any] = {}
    context["TAGS"] = []
    tags = get_tags(repo, tags_regex)
    if unreleased:
        tags.append(None)
    for tag in tags:
        duplicates = {}
        if tag is None:
            tag_name = "unreleased"
            tag_date = "unreleased"
        else:
            tag_name = tag.name
            tag_date = tag.object.authored_date
        context_tag: Dict[str, Any] = {"name": tag_name, "date": tag_date}
        reverted_commits = []
        for commit in get_commits_between(repo, previous_tag, tag):
            for tmp in commit.message.splitlines():
                line = tmp.strip()
                if line.startswith("This reverts commit "):
                    sha = line.replace("This reverts commit ", "").split(".")[0]
                    reverted_commits.append(sha)
        categories: Dict[str, List[Dict[str, str]]] = {}
        for commit in get_commits_between(repo, previous_tag, tag):
            if commit.hexsha in reverted_commits:
                continue
            for tmp in commit.message.splitlines():
                line = tmp.strip()
                cat: Optional[str] = None
                if line.startswith("feat:"):
                    cat = "New features"
                elif line.startswith("fix:"):
                    cat = "Fixes"
                if cat is not None:
                    if cat not in categories:
                        categories[cat] = []
                    entry_desc = ": ".join(line.split(": ")[1:])
                    if remove_duplicates_entries and entry_desc in duplicates:
                        continue
                    duplicates[entry_desc] = True
                    categories[cat].append(
                        {"description": entry_desc, "sha": commit.hexsha}
                    )
        context_tag["categories"] = categories
        context["TAGS"].append(context_tag)
        previous_tag = tag
    print(render_template(context))


if __name__ == "__main__":
    typer.run(main)
