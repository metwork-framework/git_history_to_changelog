import datetime

from pydantic import BaseModel


class Tag(BaseModel):

    name: str
    tagged_date: datetime.datetime

    class Config:
        frozen = True


class SpecialTag(Tag):
    pass


class HeadTag(SpecialTag):

    name: str = "__head"
    tagged_date: datetime.datetime = datetime.datetime(2999, 1, 1)


class BeginningTag(SpecialTag):

    name: str = "__beginning"
    tagged_date: datetime.datetime = datetime.datetime(1970, 1, 1)
