import datetime
import typing

from pydantic import BaseModel


class UserInternal(BaseModel):
    username: str
    creation_time: datetime.datetime


class UserRepository:
    users: typing.Dict[str, UserInternal]

    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if self.users[username]:
            raise ValueError(f"Username {username} already taken")

        creation_time = datetime.datetime.now()
        self.users[username] = UserInternal(
            username=username,
            creation_time=creation_time
        )
        return creation_time

    def get_user(self, username):
        return self.users[username]

    def list_users(self):
        return self.users.values()
