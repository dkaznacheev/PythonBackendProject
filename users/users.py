import datetime
import typing

from pydantic import BaseModel


class User(BaseModel):
    username: str
    creation_time: datetime.datetime


class UserRepository:
    users: typing.Dict[str, User]

    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            raise ValueError(f"Username {username} already taken")

        creation_time = datetime.datetime.now()
        self.users[username] = User(
            username=username,
            creation_time=creation_time
        )
        return creation_time

    def get_user(self, username):
        return self.users[username]

    def list_users(self):
        return self.users.values()
