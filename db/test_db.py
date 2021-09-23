import datetime
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

    def test_feed_newer_than(self):
        posts = PostRepository()
        posts.add_post("user1", "text1")
        time = datetime.datetime.now()
        posts.add_post("user2", "text2")
        feed = posts.get_posts(newer_than=time)
        self.assertEqual(1, len(feed))
        post = feed[0]
        self.assertEqual(1, post.id)
        self.assertEqual("user2", post.username)
        self.assertEqual("text2", post.text)
        self.assertTrue(post.creation_time >= time)

    def test_feed_of_user(self):
        posts = PostRepository()
        posts.add_post("user1", "text1")
        posts.add_post("user2", "text2")
        feed = posts.get_posts(for_user="user1")
        self.assertEqual(1, len(feed))
        post = feed[0]
        self.assertEqual(0, post.id)
        self.assertEqual("user1", post.username)
        self.assertEqual("text1", post.text)

    def test_no_like_post(self):
        posts = PostRepository()
        posts.add_post("user1", "text1")
        feed = posts.get_posts()
        self.assertEqual(0, feed[0].likes)

    def test_like_post(self):
        posts = PostRepository()
        post_id = posts.add_post("user1", "text1")
        posts.like_post(post_id)
        feed = posts.get_posts()
        self.assertEqual(1, feed[0].likes)

    def test_like_post_twice(self):
        posts = PostRepository()
        post_id = posts.add_post("user1", "text1")
        posts.like_post(post_id)
        feed = posts.get_posts()
        self.assertEqual(1, feed[0].likes)
        posts.like_post(post_id)
        feed = posts.get_posts()
        self.assertEqual(2, feed[0].likes)

    def test_like_different_posts(self):
        posts = PostRepository()
        post_id_1 = posts.add_post("user1", "text1")
        post_id_2 = posts.add_post("user2", "text2")
        posts.like_post(post_id_1)
        feed = posts.get_posts()
        self.assertEqual(1, feed[0].likes)
        self.assertEqual(0, feed[1].likes)
        posts.like_post(post_id_2)
        feed = posts.get_posts()
        self.assertEqual(1, feed[0].likes)
        self.assertEqual(1, feed[1].likes)
