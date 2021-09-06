import datetime

from fastapi import FastAPI
from typing import List
from data import Post, PostRequest

app = FastAPI()

posts: List[Post] = []
post_counter: int = 0


@app.get("/feed", response_model=List[Post])
async def feed():
    return posts


@app.post("/posts/")
async def send_post(request: PostRequest):
    global post_counter
    post_counter += 1
    posts.append(Post(id=post_counter,
                      username=request.username,
                      text=request.text,
                      creation_time=datetime.datetime.now()))
