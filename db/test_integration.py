from unittest import TestCase

from comments import CommentRepository
from db.posts import PostRepository


class TestIntegration(TestCase):
    def test_comments_are_empty(self):
        posts = PostRepository()
        comments = CommentRepository(posts)
        self.assertEqual(0,
                         len(comments.get_comments()),
                         "There should be no comments at the start")

    def test_add_post_and_comment(self):
        posts = PostRepository()
        comments = CommentRepository(posts)
        post_id = posts.add_post("test_user", "post text")
        comments.add_comment(post_id, "test_user", "comment text")
        post_comments = comments.get_comments(post_id)
        self.assertEqual(1, len(post_comments))
        comment = post_comments[0]
        self.assertEqual("test_user", comment.username)
        self.assertEqual("comment text", comment.text)
        self.assertEqual(0, comment.id)

    def test_post_not_exists(self):
        posts = PostRepository()
        comments = CommentRepository(posts)
        post_id = posts.add_post("test_user", "post text")
        try:
            comments.add_comment(post_id + 1, "test_user", "comment text")
            self.fail()
        except FileNotFoundError as e:
            pass
