from fastapi import FastAPI
from typing import List
from data import Post, PostRequest
from db import PostRepository

app = FastAPI()

posts = PostRepository()


@app.get("/feed", response_model=List[Post])
async def feed():
    return posts.get_posts()


@app.post("/posts/")
async def send_post(request: PostRequest):
    posts.add_post(request.username, request.text)
