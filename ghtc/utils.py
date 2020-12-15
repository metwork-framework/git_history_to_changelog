from typing import List, Optional
import os
import jinja2
from git import Repo, Tag, Commit
import re

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TagNotFound(Exception):

    pass


def get_tags(repo: Repo, tag_regex: str) -> List[Tag]:
    compiled_pattern = re.compile(tag_regex)
    res = []
    for tag in repo.tags:
        if re.match(compiled_pattern, tag.name):
            res.append(tag)
    return res


def get_commits_between(repo: Repo, rev1: str = None, rev2: str = None) -> List[Commit]:
    kwargs = {}
    if rev1 is not None or rev2 is not None:
        tag1_name = "" if rev1 is None else rev1
        tag2_name = "HEAD" if rev2 is None else rev2
        kwargs["rev"] = f"{tag1_name}..{tag2_name}"
    return list(repo.iter_commits(**kwargs))


def render_template(context, template_file: str = None) -> str:
    if template_file is not None:
        template_to_read = template_file
    else:
        template_to_read = f"{CURRENT_DIR}/CHANGELOG.md"
    with open(template_to_read, "r") as f:
        content = f.read()
    template = jinja2.Template(content)
    return template.render(context)


def get_reverted_commit(commit: Commit) -> Optional[str]:
    for tmp in commit.message.splitlines():
        line = tmp.strip()
        if line.startswith("This reverts commit "):
            sha = line.replace("This reverts commit ", "").split(".")[0]
            if len(sha) >= 40:
                return sha
    return None
