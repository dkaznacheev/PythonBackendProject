import grpc
from fastapi import FastAPI
from typing import List
from postcount_pb2_grpc import PostCounterStub
import postcount_pb2 as postcount
from data import Post, PostRequest
from db.db import PostRepository

app = FastAPI()

posts = PostRepository()
grpc_channel = grpc.insecure_channel('localhost:50051')
postcount_stub = PostCounterStub(grpc_channel)


@app.get("/feed", response_model=List[Post])
async def feed():
    return posts.get_posts()


@app.post("/posts/", response_model=int)
async def send_post(request: PostRequest):
    post_id = posts.add_post(request.username, request.text)
    postcount_stub.PostMessage(
        postcount.Post(id=post_id, username=request.username))
    return post_id


@app.on_event("shutdown")
async def on_shutdown():
    grpc_channel.close()
