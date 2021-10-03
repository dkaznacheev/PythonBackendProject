import datetime
import typing

import strawberry


@strawberry.type
class PostModel:
    id: int
    username: str
    text: str
    creation_time: datetime.datetime
    likes: int


@strawberry.type
class UserModel:
    username: str
    posts: typing.List[PostModel]
    creation_time: datetime.datetime


def to_post_model(posts):
    return [PostModel(id=post.id,
                      username=post.username,
                      text=post.text,
                      creation_time=post.creation_time,
                      likes=post.likes) for post in posts]
