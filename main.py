import datetime

import grpc
from fastapi import FastAPI, HTTPException
from typing import List
from postcount_pb2_grpc import PostCounterStub
from data import Post, PostRequest
from db.db import PostRepository

app = FastAPI()

posts = PostRepository()
grpc_channel = grpc.insecure_channel('localhost:50051')
postcount_stub = PostCounterStub(grpc_channel)


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
    # not needed in this hw
    # postcount_stub.PostMessage(
    #     postcount.Post(id=post_id, username=request.username))
    return post_id


@app.on_event("shutdown")
async def on_shutdown():
    grpc_channel.close()
