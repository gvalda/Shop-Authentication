from dataclasses import dataclass
import uuid


class Event:
    pass


@dataclass
class UserCreated(Event):
    id: uuid.uuid4
    username: str
    email: str


@dataclass
class UserEmailVerified(Event):
    id: uuid.uuid4


@dataclass
class UserBanned(Event):
    id: uuid.uuid4


@dataclass
class UserUnBanned(Event):
    id: uuid.uuid4


@dataclass
class UserDeleted(Event):
    id: uuid.uuid4
