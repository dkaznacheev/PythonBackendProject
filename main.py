import datetime
import typing
from typing import List

import strawberry
from fastapi import FastAPI, HTTPException
from strawberry import Schema
from strawberry.asgi import GraphQL

from data import Post, PostRequest
from db.comments import CommentRepository
from db.posts import PostRepository
from users.users import UserRepository

app = FastAPI()

posts = PostRepository()
comments = CommentRepository(posts)
users = UserRepository()


@strawberry.type
class User:
    username: str
    posts: typing.List[Post]
    creation_time: datetime.datetime


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> typing.List[User]:
        return [User(
            username=user.username,
            posts=posts.get_posts(for_user=user.username),
            creation_time=user.creation_time
        ) for user in users.list_users()]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, username: str) -> User:
        creation_time = users.add_user(username)
        return User(
            username=username,
            posts=[],
            creation_time=creation_time
        )


schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app.add_route("/users", graphql_app)
app.add_websocket_route("/users", graphql_app)


@app.get("/feed", response_model=List[Post])
async def global_feed(
        for_user: str = None,
        newer_than: datetime.datetime = None
):
    return posts.get_posts(for_user, newer_than)


@app.post("/posts/{post_id}/like/")
async def like(post_id: int):
    if posts.like_post(post_id):
        return
    else:
        raise HTTPException(status_code=404, detail="Post not found")


@app.post("/posts/", response_model=int)
async def send_post(request: PostRequest):
    post_id = posts.add_post(request.username, request.text)
    return post_id


@app.get("/posts/{post_id}/comments/")
async def get_comments(post_id: int):
    return comments.get_comments(post_id)


@app.post("/posts/{post_id}/comments/")
async def add_comment(post_id: int, request: PostRequest):
    return comments.add_comment(post_id, request.username, request.text)
