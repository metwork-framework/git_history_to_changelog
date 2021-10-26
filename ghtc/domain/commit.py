import datetime

from pydantic import BaseModel


class Commit(BaseModel):

    hexsha: str
    date: datetime.datetime
    message: str
