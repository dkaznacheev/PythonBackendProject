import datetime
from unittest import TestCase

import main
from data import PostRequest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def create_post(user_id):
    return client.post("/posts/", json=PostRequest(
        username="user" + str(user_id),
        text="text" + str(user_id)
    ).dict())


class TestIntegrationApp(TestCase):
    def setUp(self):
        # man i love no private fields
        main.posts.posts.clear()
        main.posts.post_counter = 0

    def test_create_post(self):
        response = create_post(1)
        self.assertEqual(200, response.status_code)
        self.assertEqual("0", response.text)
        response = create_post(2)
        self.assertEqual(200, response.status_code)
        self.assertEqual("1", response.text)
        response = client.get("/feed/")
        self.assertEqual(200, response.status_code)
        posts = response.json()
        self.assertEqual(2, len(posts))
        self.assertEqual("user1", posts[0]["username"])
        self.assertEqual("text1", posts[0]["text"])
        self.assertEqual(0, posts[0]["id"])
        self.assertEqual("user2", posts[1]["username"])
        self.assertEqual("text2", posts[1]["text"])
        self.assertEqual(1, posts[1]["id"])

    def test_filter_posts(self):
        create_post(1)
        time = datetime.datetime.now()
        create_post(2)

        response = client.get("/feed", params={"newer_than": time})
        self.assertEqual(200, response.status_code)
        feed = response.json()
        self.assertEqual(1, len(feed))
        post = feed[0]
        self.assertEqual("user2", post["username"])
        self.assertEqual("text2", post["text"])
        self.assertEqual(1, post["id"])

        response = client.get("/feed/", params={"for_user": "user1"})
        self.assertEqual(200, response.status_code)
        feed = response.json()
        self.assertEqual(1, len(feed))
        post = feed[0]
        self.assertEqual("user1", post["username"])
        self.assertEqual("text1", post["text"])
        self.assertEqual(0, post["id"])

    def test_like_post(self):
        create_post(1)
        create_post(2)

        client.post("/posts/", json=PostRequest(
            username="user2",
            text="text2"
        ).dict())

        response = client.get("/feed/")
        self.assertEqual(200, response.status_code)
        posts = response.json()
        self.assertEqual(0, posts[0]["likes"])
        self.assertEqual(0, posts[1]["likes"])

        client.post("/posts/1/like/")
        posts = client.get("/feed/").json()
        self.assertEqual(0, posts[0]["likes"])
        self.assertEqual(1, posts[1]["likes"])
