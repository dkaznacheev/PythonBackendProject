import datetime
from typing import List

from data import Post


# Here be database layer
class PostRepository:
    posts: List[Post]
    post_counter: int

    def __init__(self):
        self.posts = []
        self.post_counter = 0

    def get_posts(self):
        return self.posts

    def add_post(self, username, text):
        self.posts.append(Post(id=self.post_counter,
                               username=username,
                               text=text,
                               creation_time=datetime.datetime.now()))
        self.post_counter += 1
        return self.post_counter
