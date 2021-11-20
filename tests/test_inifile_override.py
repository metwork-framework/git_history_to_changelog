import os
import tempfile

from mfutil import get_unique_hexa_identifier

from ghtc.app.parser import ParserController
from ghtc.domain.changelog import ChangelogEntryType
from ghtc.infra.override.inifile import OverrideInifileBackend
from ghtc.infra.parser import ALL_PARSERS


PARSE1 = """
[123456]
feat: this is a test

Close: #456

[aaaaaa]
fix: this is another test

[bbbbbb]


"""

parserc = ParserController(ALL_PARSERS)


def make_tmp_filepath(content: str):
    path = os.path.join(tempfile.gettempdir(), get_unique_hexa_identifier())
    with open(path, "w") as f:
        f.write(content)
    return path


def test_not_found():
    x = OverrideInifileBackend("/foo/bar/not_found", parserc)
    assert len(x.overrides) == 0


def test_parse1():
    path = make_tmp_filepath(PARSE1)
    x = OverrideInifileBackend(path, parserc)
    assert len(x.overrides) == 3
    assert x.overrides["123456"][0].type == ChangelogEntryType.ADDED
    assert x.overrides["123456"][0].message == "this is a test"
    assert x.overrides["aaaaaa"][0].type == ChangelogEntryType.FIXED
    assert x.overrides["aaaaaa"][0].message == "this is another test"
    assert x.overrides["bbbbbb"] == []
    os.unlink(path)
