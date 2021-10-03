import datetime

import strawberry
from pydantic import BaseModel


@strawberry.type
class Post(BaseModel):
    id: int
    username: str
    text: str
    creation_time: datetime.datetime
    likes: int


@strawberry.type
class Comment(BaseModel):
    id: int
    post_id: int
    username: str
    text: str
    creation_time: datetime.datetime


class PostRequest(BaseModel):
    username: str
    text: str
