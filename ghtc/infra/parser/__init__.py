from ghtc.infra.parser.conventional import ParserConventionalBackend
from ghtc.infra.parser.ghtc import ParserGhtcBackend
from ghtc.infra.parser.gitlab import ParserGitlabBackend


ALL_PARSERS = [ParserConventionalBackend(), ParserGitlabBackend(), ParserGhtcBackend()]
