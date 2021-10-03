import datetime

from fastapi import FastAPI, HTTPException
from typing import List
from data import Post, PostRequest
from db.comments import CommentRepository
from db.posts import PostRepository

app = FastAPI()

posts = PostRepository()
comments = CommentRepository(posts)


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
