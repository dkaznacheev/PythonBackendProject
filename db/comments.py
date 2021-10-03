import datetime
from collections import defaultdict

from data import Comment
from db.posts import PostRepository


class CommentRepository:
    comment_counter: int
    post_repo: PostRepository

    def __init__(self, post_repo):
        self.comments = defaultdict(list)
        self.comment_counter = 0
        self.post_repo = post_repo

    def get_comments(self, post_id=None):
        if post_id is None:
            return sum(self.comments.values(), [])
        return self.comments[post_id]

    def add_comment(self, post_id, username, text):
        self.comments[post_id].append(Comment(id=self.comment_counter,
                                              post_id=post_id,
                                              username=username,
                                              text=text,
                                              creation_time=datetime.datetime.now()))
        if not self.post_repo.contains_post(post_id):
            raise FileNotFoundError

        self.comment_counter += 1
        return self.comment_counter - 1

