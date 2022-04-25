from uuid import uuid4
from typing import List

from authentication.domain import events


class BaseModel:
    pass


class User(BaseModel):
    def __init__(
            self,
            id: uuid4,
            username: str,
            password: str,
            email: str,
            is_admin: bool = False,
            is_verified: bool = False,
            is_banned: bool = False,
            is_deleted: bool = False,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.is_verified = is_verified
        self.is_banned = is_banned
        self.is_deleted = is_deleted
        self.events = []  # type: List[events.Event]

        self.events.append(events.UserCreated(
            id=self.id,
            username=self.username,
            email=self.email,
        ))

    def verify(self):
        self.is_verified = True
        self.events.append(events.UserEmailVerified(
            id=self.id,
        ))

    def ban(self):
        self.is_banned = True
        self.events.append(events.UserBanned(
            id=self.id,
        ))

    def unban(self):
        self.is_banned = False
        self.events.append(events.UserUnBanned(
            id=self.id,
        ))

    def delete(self):
        self.is_deleted = True
        self.events.append(events.UserDeleted(
            id=self.id,
        ))
