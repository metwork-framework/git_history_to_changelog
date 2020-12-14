from typing import List
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


def get_tag(repo: Repo, tag_name: str = None) -> Tag:
    if tag_name is None:
        return None
    for tag in repo.tags:
        if tag.name == tag_name:
            return tag
    raise TagNotFound(f"tag: {tag_name} not found")


def get_commits_between(repo: Repo, tag1: Tag, tag2: Tag = None) -> List[Commit]:
    kwargs = {}
    if tag1 is not None or tag2 is not None:
        tag1_name = "" if tag1 is None else tag1.name
        tag2_name = "HEAD" if tag2 is None else tag2.name
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
