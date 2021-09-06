import datetime
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    username: str
    text: str
    creation_time: datetime.datetime


class PostRequest(BaseModel):
    username: str
    text: str
