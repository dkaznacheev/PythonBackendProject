from unittest import TestCase

from db import PostRepository


class TestPostRepository(TestCase):
    def test_posts_are_empty(self):
        posts = PostRepository()
        self.assertEqual(0,
                         len(posts.get_posts()),
                         "There should be no posts at the start")

    def test_add_post(self):
        posts = PostRepository()
        posts.add_post("test_user", "template_text")
        feed = posts.get_posts()
        self.assertEqual(1, len(feed), "There should be 1 post in the feed")
        post = feed[0]
        self.assertEqual("test_user", post.username)
        self.assertEqual("template_text", post.text)
        self.assertEqual(0, post.id)

    def test_posts_chronologically_ordered(self):
        posts = PostRepository()
        posts.add_post("user1", "text1")
        posts.add_post("user2", "text2")
        feed = posts.get_posts()
        self.assertEqual(0, feed[0].id)
        self.assertEqual(1, feed[1].id)
        self.assertTrue(feed[0].creation_time < feed[1].creation_time)
