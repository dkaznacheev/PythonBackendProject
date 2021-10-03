from unittest import TestCase

from comments import CommentRepository
from db.posts import PostRepository


def setup_posts(ids=None):
    if ids is None:
        ids = []
    posts = PostRepository()
    posts.contains_post = lambda post: post in ids
    return posts


class TestCommentRepository(TestCase):
    def test_comments_are_empty(self):
        comments = CommentRepository(setup_posts())
        self.assertEqual(0,
                         len(comments.get_comments()),
                         "There should be no comments at the start")

    def test_add_comment(self):
        comments = CommentRepository(setup_posts([1]))
        comments.add_comment(1, "test_user", "template_text")
        post_comments = comments.get_comments(1)
        self.assertEqual(1, len(post_comments))
        comment = post_comments[0]
        self.assertEqual("test_user", comment.username)
        self.assertEqual("template_text", comment.text)
        self.assertEqual(0, comment.id)

    def test_comments_chronologically_ordered(self):
        comments = CommentRepository(setup_posts([1]))
        comments.add_comment(1, "user1", "text1")
        comments.add_comment(1, "user2", "text2")
        post_comments = comments.get_comments(1)
        self.assertEqual(0, post_comments[0].id)
        self.assertEqual(1, post_comments[1].id)
        self.assertTrue(post_comments[0].creation_time < post_comments[1].creation_time)

    def test_no_post_exists(self):
        comments = CommentRepository(setup_posts())
        try:
            comments.add_comment(123, "user", "text")
            self.fail()
        except FileNotFoundError as e:
            pass
