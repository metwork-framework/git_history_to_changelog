import datetime
from enum import Enum, auto
from typing import List, Optional

from pydantic import BaseModel


class Commit(BaseModel):

    hexsha: str
    committed_date: datetime.datetime
    message: str


class ConventionalCommitType(Enum):

    OTHER = auto()
    BUILD = auto()
    CHORE = auto()
    STYLE = auto()
    CI = auto()
    REFACTOR = auto()
    TEST = auto()
    DOCS = auto()
    PERF = auto()
    FIX = auto()
    FEAT = auto()


class ConventionalCommitFooter(BaseModel):

    key: str
    value: str

    class Config:
        frozen = True


class ConventionalCommitMessage(BaseModel):

    type: ConventionalCommitType
    description: str
    breaking: bool = False
    scope: Optional[str] = None
    body: Optional[str] = None
    footers: List[ConventionalCommitFooter] = []

    class Config:
        frozen = True
