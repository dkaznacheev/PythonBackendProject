import datetime
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    username: str
    text: str
    creation_time: datetime.datetime
    likes: int


class PostRequest(BaseModel):
    username: str
    text: str


class Comment(BaseModel):
    id: int
    post_id: int
    username: str
    text: str
    creation_time: datetime.datetime
