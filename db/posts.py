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

    def get_posts(self, for_user = None, newer_than = None):
        feed = self.posts
        if for_user:
            feed = [post for post in feed if post.username == for_user]
        if newer_than:
            feed = [post for post in feed if post.creation_time >= newer_than]
        return feed

    def add_post(self, username, text):
        self.posts.append(Post(id=self.post_counter,
                               username=username,
                               text=text,
                               creation_time=datetime.datetime.now(),
                               likes=0))
        self.post_counter += 1
        return self.post_counter - 1

    def like_post(self, post_id):
        post = next((x for x in self.posts if x.id == post_id), None)
        if post is None:
            return False
        post.likes += 1
        return True

    def contains_post(self, post_id):
        for post in self.posts:
            if post.id == post_id:
                return True
        return False